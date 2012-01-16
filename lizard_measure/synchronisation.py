# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

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


def _to_float_or_none(xml_str):
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


def get_aquo_domain_table_xml(model,
                              page_size=0,
                              start_page=0,
                              check_date=None):
    """
    Return soap xml for aquo domain table

    Set page_size to 0 to get all records on a single page. Set start_page
    to start the page at another item.
    """
    domain_table = model.get_sync_info().source_table
    client = Client('http://domeintabellen-idsw-ws.rws.nl/DomainTableWS.svc?wsdl')
    client.set_options(retxml=True)  # Only give xml, since there is a tokenizing problem
                                     # Will do the parsing manually with lxml
    request = client.factory.create('ns1:GetDomainTableRequest')
    
    request.DomaintableName = domain_table
    request.PageSize = page_size
    request.StartPage = start_page

    if check_date is None:
        check_date = datetime.datetime.today()
    request.CheckDate = check_date
    
    xml_and_headers = client.service.GetDomainTable(request=request)
    xml = xml_and_headers.splitlines()[-2]

    return xml


def aquo_xml_to_python(xml, model):
    """ Return dictionary with relevant properties from aquo domain table.

    The 'Data'-value itself is a dictionary based on the sync_field from the sync_info.
    """
    reverse_mapper = dict(
        [(v, k) 
         for k, v in model.get_sync_info().mapper.iteritems()],
    )
    sync_field_aquo = reverse_mapper[model.get_sync_info().sync_field]

    root = etree.fromstring(xml)

    # get all namespaces defined in document
    namespaces = {}
    for e in root.iter():
        namespaces.update(e.nsmap)

    # Make default namespace explicit since xpath does
    # not handle empty namespace prefixes
    namespaces['d'] = namespaces[None]
    del namespaces[None]

    xpath_base = '/s:Envelope/s:Body/*/*/'

    # Fill the statistics
    aquo_data = {}
    aquo_data['Data'] = {}
    for t in [
        'DataRowsReadPage',  # Records retrieved
        'PageSize',  # Maximum of records per page as requested
        'TotalDataRows',  # In the table
    ]:
        xpath = xpath_base + 'a:' + t
        element = root.xpath(xpath, namespaces=namespaces)[0]
        aquo_data[t] = int(element.text)

    # Iterate over the datarows
    xpath_data_rows = xpath_base + 'a:Data/a:DataRow'
    data_rows = root.xpath(
        xpath_data_rows,
        namespaces=namespaces
    )
    for data_row in data_rows:

        # Store the fields of a row in a dict, with the aquo_sync_field as key
        data_fields = data_row.findall(
            'a:Fields/a:DataField',
            namespaces=namespaces,
        )
        result_row = {}
        for field in data_fields:
            field_key = field.find('a:Name', namespaces=namespaces).text
            field_value = field.find('a:Data', namespaces=namespaces).text
            result_row[field_key] = field_value
        row_key = result_row[sync_field_aquo]
            
        aquo_data['Data'][row_key] = result_row

    return aquo_data

def update_model_from_aquo_data(
        model,
        aquo_data,
        invalidate=True,
    ):
    """
    Update django model from dictionary object according to mapping.

    Note that the mapping is stored on the model itself. It needs to
    implement a get_aquo_sync_info classmethod, returning an AquoSyncInfo
    object.

    When invalidate == True, the valid field of entries not in the
    dictionary object are set to 'False'.
    """
    sync_field = model.get_sync_info().sync_field
    mapper = model.get_sync_info().mapper

    if isinstance(model._meta.get_field(sync_field), models.IntegerField):
        raise NotImplementedError('Integer sync_field!')
    for sync_field_aquo, aquo_row in aquo_data['Data'].iteritems():
        get_kwargs = {sync_field: sync_field_aquo}
        try:
            instance = model.objects.get(**get_kwargs)
        except model.DoesNotExist:
            instance = model()


        for aquo_name, aquo_value in aquo_row.iteritems():
            field_name = mapper[aquo_name]
            if isinstance(model._meta.get_field(field_name),
                          models.FloatField):
                field_value = _to_float_or_none(aquo_value)
            else:
                field_value = aquo_value
                            
            
            setattr(instance, field_name, field_value)
            instance.valid = True
        instance.save()

    if invalidate:
        exclude_kwargs = {sync_field + '__in': aquo_data['Data']}
        for instance in model.objects.exclude(**exclude_kwargs):
            instance.valid = False
            instance.save()
        
        
def execute_sync(model, invalidate=True):
    logger.debug('Syncing %s' % model )

    logger.debug('Getting xml...')
    xml = get_aquo_domain_table_xml(model)
    aquo_data = aquo_xml_to_python(xml, model)
    logger.debug('Updating database...')
    update_model_from_aquo_data(model, aquo_data, invalidate=invalidate)
