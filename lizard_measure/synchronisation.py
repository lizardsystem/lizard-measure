# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-
"""
Enable synchronisation of models from aquo domaintables. A few prerequisites on the model:
- Model should inherit from SyncableMixin
- Model should define a NullBooleanField named 'valid'
- Model should define a classmethod 'get_sync_config' that looks like this:

TODO.

"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models

from lizard_measure.utils import get_or_create
from suds.client import Client
from lxml import etree

import datetime
import logging
import pprint

logging.getLogger('suds').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class SyncField(object):
    """ 
    Describe the relation between a source and a destination field
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
                 sync_fields,
                 source_table,
                 source_type='Aquo'):
        self.model = model
        self.source_type = source_type
        self.sync_fields = sync_fields
        self.source_table = source_table
        self.data = None  # To be filled by synchronizer

    @property
    def match_fields(self):
        return [sf.destination for sf in self.sync_fields if sf.match]

class Synchronizer(object):
    """
    Container for all synchronization methods and functions
    """
    
    AQUO_URL = 'http://domeintabellen-idsw-ws.rws.nl/DomainTableWS.svc?wsdl'

    def __init__(self, model, sources, invalidate=True):
        self.model = model
        self.sources = sources
        self.invalidate = invalidate


    def get_aquo_xml(self, table, page_size=0, start_page=0, check_date=None):
        """
        Return soap xml for aquo domain table

        Set page_size to 0 to get all records on a single page. Set start_page
        to start the page at another item.
        """
        client = Client(self.AQUO_URL)

        # Because the suds client fails to tokenize (pythonize) the returned xml
        # Correctly, we need to do it manually via lxml / etree. The following option
        # Instructs suds just to return the xml without tokenizing.
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


    def _get_name_spaces(root, default_namespace='d'):
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

    def _check_aquo_statistics(root, namespaces):
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
        logger.debug('Getting data for aquo table %s' % domain_table)
        logger.debug('get')
        xml = get_aquo_xml(table)
        logger.debug('parse')
        root = etree.fromstring(xml)
        logger.debug('nsmap')
        namespaces = _get_name_spaces(root)
        logger.debug('check')
        _check_aquo_statistics(root, namespaces)
        logger.debug('pythonize')

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

    def _defaults_and_get_kwargs(self, source, record):
        """
        Return get_kwargs, defaults for use in get_or_create.

        Prepares the mapping between data and model, doing necessary
        conversion and filling in static values, where configured
        according to source.fields
        """
        match_fields = source.match_fields

        for sf in self.sync_fields:
            key = sf.destination

            # Imported value or static value?
            if sf.static:
                value = sf.source
            else:
                value = record[sf.source]

            # Need some conversions?
            if isinstance(self.model._meta.get_field(sf.destination),
                          models.FloatField):
                value = self._to_float_or_none(value)

            # Match field or not?
            if key in match_fields:
                get_kwargs[key] = value
            else:
                defaults[key] = value

            defaults.valid = True

        return get_kwargs, defaults

    def sync_objects(self, source):
        """
        Get and update, or create a model object from record
        """
        logger.debug('Updating database...')

        for record in data:
            get_kwargs, defaults = self.defaults_and_get_kwargs(
                source,
                record,
            )

            obj, created = self.model.get_or_create(defaults=defaults,
                                                    **get_kwargs)

            if not created:
                for k, v in defaults:
                    setattr(obj, k, v)

    def synchronize_source(self, source):
        """
        Synchronize model from a single source
        """
        if source.source_type=='Aquo':
            source.data = self.load_aquo_data(source.source_table)
        else:
            raise NotImplementedError('Unknown source type')

        self.sync_objects(source)


    def synchronize(self, invalidate=True):
        """
        Synchronize model from all sources
        """

        self.unsynced_objects = self.model.objects.all()

        for source in self.sources:
            synchronize_source(source)
            
        if self.invalidate:
            synchronizer.invalidate()


    def invalidate_out_of_sync(cls, data):
        """
        Set objects to invalid that were not synced.
        """
        logger.debug('Invalidating out of sync objects...')
