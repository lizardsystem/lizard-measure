# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-
"""
Enable synchronisation of models from aquo domaintables. A few
prerequisites on the model:
- Model should define a NullBooleanField named 'valid'
- Model should define a classmethod 'get_synchronizer'
  that returns a configured Synchronizer object, for example:

    @classmethod
    def get_synchronizer(cls):
        fields = [
            SyncField(source='Code', destination='code', match=True),
            SyncField(source='Omschrijving', destination='description'),
        ]

        sources = [SyncSource(
                            model=cls,
                            source_table='KRWStatus',
                            fields=fields,
                        )]

        return Synchronizer(sources=sources)
"""
from django.db import models

from suds.client import Client
from lxml import etree

import datetime
import logging

logging.getLogger('suds').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class SyncField(object):
    """
    Describe the relation between a source and a destination field.

    If a field is static, it is used to identify a subset of objects
    to invalidate if not synced.
    """
    def __init__(self, source, destination, static=False, match=False):
        self.source = source
        self.destination = destination
        self.static = static
        self.match = match


class SyncSource(object):
    """
    Describe de relation between a source and a destination record
    """
    def __init__(self,
                 model,
                 fields,
                 source_table,
                 source_type='Aquo'):
        self.model = model
        self.source_type = source_type
        self.fields = fields
        self.source_table = source_table
        self.data = None  # To be filled by synchronizer

    def _to_float_or_none(self, xml_str):
        """
        Return float from str, replacing ',' by '.'.

        Return None if xml_str is None or unintelligible.
        """
        if xml_str is None:
            return None
        else:
            try:
                return float(xml_str.replace(',', '.'))
            except ValueError:
                return None

    def _to_integer_or_none(self, xml_str):
        """
        Return integer from str.

        Return None if xml_str is None or unintelligible.
        """
        if xml_str is None:
            return None
        else:
            try:
                return int(xml_str)
            except ValueError:
                return None

    def _convert(self, value, field):
        """
        Return converted value suitable for field
        """
        if isinstance(self.model._meta.get_field(field),
                      models.FloatField):
            return self._to_float_or_none(value)
        if isinstance(self.model._meta.get_field(field),
                      models.IntegerField):
            return self._to_integer_or_none(value)
        else:
            return value

    def object_kwargs(self):
        """
        Return generator of (filter_kwargs, update_kwargs, create_kwargs)

        To be used filter, create and update statements. These
        keyword arguments are prepared using the data from the source
        record. Prerequisite is that self.data is already filled.
        """
        for record in self.data:

            filter_kwargs = {}
            update_kwargs = {}
            create_kwargs = {}

            for field in self.fields:
                key = field.destination

                # Imported value or static value?
                if field.static:
                    value = field.source
                else:
                    value = self._convert(
                        value=record[field.source],
                        field=field.destination,
                    )

                # Add to the right kwargs
                create_kwargs[key] = value
                if field.match:
                    filter_kwargs[key] = value
                else:
                    update_kwargs[key] = value

            yield filter_kwargs, update_kwargs, create_kwargs

    def source_kwargs(self):
        """
        Return kwargs to use in filter statement to exclude objects that
        are not synchronized using this source. Currently uses fields
        with static=True for this.
        """
        return dict([(f.destination, f.source)
                     for f in self.fields
                     if f.static])

    def compare_kwargs(self, object):
        """
        Return keyword arguments for an existing object.

        Useful for comparing with generated keyword arguments to see if
        an object was actually synced.
        """
        result = {}
        for field in self.fields:
            result[field.destination] = getattr(object, field.destination)

        return result


class Synchronizer(object):
    """
    Performs actual synchronization
    """

    AQUO_URL = 'http://domeintabellen-idsw-ws.rws.nl/DomainTableWS.svc?wsdl'

    def __init__(self, sources):
        self.sources = sources

    def _load_aquo_xml(self,
                       table,
                       page_size=0,
                       start_page=0,
                       check_date=None):
        """
        Return soap xml for aquo domain table

        Set page_size to 0 to get all records on a single page. Set start_page
        to start the page at another item.
        """
        client = Client(self.AQUO_URL)

        # Because the suds client fails to tokenize (pythonize) the
        # returned xml Correctly, we need to do it manually via lxml /
        # etree. The following option Instructs suds just to return the
        # xml without tokenizing.
        client.set_options(retxml=True)

        request = client.factory.create('ns1:GetDomainTableRequest')

        request.DomaintableName = table
        request.PageSize = page_size
        request.StartPage = start_page
        if check_date is None:
            check_date = datetime.datetime.today()
        request.CheckDate = check_date

        xml_and_headers = client.service.GetDomainTable(request=request)
        xml = xml_and_headers.splitlines()[-2]

        return xml

    def _get_name_spaces(self, root, default_namespace='d'):
        """
        Iterate tree and return all namespaces.

        Default namespace is made explicit with key default_namespace
        """
        # get all namespaces defined in document
        namespaces = {}
        for e in root.iter():
            namespaces.update(e.nsmap)

        # Make default namespace explicit since xpath does
        # not handle empty namespace prefixes
        namespaces['d'] = namespaces[None]
        del namespaces[None]

        return namespaces

    def _check_aquo_statistics(self, root, namespaces):
        """
        Return True if amount of retrieved datarows matches total amount
        of datarows.
        """

        xpath_base = '/s:Envelope/s:Body/*/*/'
        statistics = {}

        for tag in [
            'DataRowsReadPage',  # Records retrieved
            'PageSize',  # Maximum of records per page as requested
            'TotalDataRows',  # In the table
        ]:
            xpath = xpath_base + 'a:' + tag
            element = root.xpath(xpath, namespaces=namespaces)[0]
            statistics[tag] = int(element.text)

        if not statistics['DataRowsReadPage'] == statistics['TotalDataRows']:
            raise ValueError('Not all rows were retrieved from webservice!')

    def load_aquo_data(self, table):
        """
        Return aquo data as list of dicts.
        """
        logger.debug('Getting data for aquo table %s...' % table)
        xml = self._load_aquo_xml(table)
        root = etree.fromstring(xml)
        namespaces = self._get_name_spaces(root=root)
        self._check_aquo_statistics(root=root, namespaces=namespaces)

        # Iterate over the datarows and store each row as dict
        result = []
        xpath_data_rows = '/s:Envelope/s:Body/*/*/a:Data/a:DataRow'
        data_rows = root.xpath(xpath_data_rows, namespaces=namespaces)

        for data_row in data_rows:
            data_fields = data_row.findall(
                'a:Fields/a:DataField',
                namespaces=namespaces,
            )

            result_row = {}
            for field in data_fields:
                field_key = field.find('a:Name', namespaces=namespaces).text
                field_value = field.find('a:Data', namespaces=namespaces).text
                result_row[field_key] = field_value

            result.append(result_row)

        return result

    def synchronize_objects(self, source):
        """
        Filter and update, or create model objects from source data
        """
        logger.debug('Updating database...')

        source.synced = []

        for f_kwargs, u_kwargs, c_kwargs in source.object_kwargs():

            n = source.model.objects.filter(
                **f_kwargs).update(valid=True, **u_kwargs)
            if n > 1:
                logger.warn('Synced multiple items from '
                    'a single source record!')
            elif n == 0:
                source.model.objects.create(valid=True, **c_kwargs)

            source.synced.append(c_kwargs)

    def synchronize_source(self, source):
        """
        Synchronize model from a single source
        """
        if source.source_type == 'Aquo':
            source.data = self.load_aquo_data(source.source_table)
        else:
            raise NotImplementedError('Unknown source type')

        self.synchronize_objects(source)
        self.invalidate_objects(source)

    def invalidate_objects(self, source):
        """
        Set objects to invalid that were not synced.
        """
        logger.debug('Invalidating out of sync objects...')
        for obj in source.model.objects.filter(**source.source_kwargs()):
            if not source.compare_kwargs(obj) in source.synced:
                obj.valid = False
                obj.save()

    def synchronize(self, invalidate=True):
        """
        Synchronize model from all sources
        """
        for source in self.sources:
            self.synchronize_source(source)
