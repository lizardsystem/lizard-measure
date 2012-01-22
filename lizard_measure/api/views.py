from django.core.urlresolvers import reverse
from django.db.models.fields import FieldDoesNotExist
from djangorestframework.views import View
import json
from django.db import models
from lizard_measure.models import Organization, Measure

import logging
logger = logging.getLogger(__name__)



class RootView(View):
    """
    Startpoint.
    """
    def get(self, request):
        return {
            "measure": reverse("lizard_measure_api_measure"),
            }


class OrganizationView(View):
    """
    Show organisations for selection
    """
    def get(self, request):

        start = int(request.GET.get('start', 0))
        limit = int(request.GET.get('limit', 20))
        query = request.GET.get('query', None)

        organizations = Organization.objects.filter(
                valid=True)

        if query:
            organizations = organizations.filter(name__istartswith=query)

        return {'data': [{'id': org.id,
                         'name': org.name}
                        for org in organizations.order_by(
                        'name').distinct()[start:(start + limit)]],
                'total': organizations.count()}


    """
        {
    success: true,
    data:{
        id: 1,
        ident: 'mtr33b',
        title: 'maartregel-1',
        is_krw_measure: true,
        is_indicator: false,

        measure_type: 'a',
        period: 'a',

        import_source: 'handmatig',
        import_raw: '{name: "hier staat het oude record"}',
        aggregation_type: 1,
        description: 'hier staat de beschrijving',
        categories: 'a',
        value: 33,
        unit: 'a',
        initiator: {id:2, name: 'b'},
        executive: {id:4, name: 'd'},
        responsible_department: 'afdeling b',
        total_costs: 100,
        investment_costs: 60,
        exploitation_costs: 40,
        funding_organisations: [{id:1, name: 'a', percentage: 33},{id:2, name: 'b', percentage: 33}],
        read_only: false,
        waterbodies: [{id: 163, name: "Amstellandboezem"}],
        areas: [{id: 388, name: "Aetsveldse Polder Oost"}]
    }
}
    """


class MeasureView(View):
    """
    Area configuration.
    """


    def str2float_or_none(self, value):
        """
            returns integer of value, or when not a number returns 'None'
        """
        try:
            return float(value)
        except (TypeError, ValueError):
            print 'value %s is not a number'%str(value)
            return None


    def str2int_or_none(self, value):
        """
            returns integer of value, or when not a number returns 'None'
        """
        try:
            return int(value)
        except (TypeError, ValueError):
            print 'value %s is not a number'%str(value)
            return None

    def str2bool_or_none(self, value):
        """
            returns integer of value, or when not a number returns 'None'
        """
        print value
        if type(value) == bool:
            return value
        elif type(value) in (str, unicode):
            if value.lower in ('true', '1', 'on'):
                return True
            elif value.lower in ('false', '0', 'off'):
                return False
            else:
                return None
        elif type(value) in (int, float):
            return bool(value)
        else:
            return None
        
    def get_related_objects(self, related_objects, flat=True):
        """
            get related objects (many2many field) as [{id:<> ,name:<>},{..}] or []
        """
        output = []
        print related_objects
        print related_objects.count()
        for obj in related_objects.all():
            print obj
            output.append(self.get_related_object(obj, flat))

        return output

    def get_related_object(self, related_object, flat=True):
        """
            get related object as {id:<> ,name:<>} or None of None
        """
        if related_object is None:
            return None
        else:
            if flat:
                return str(related_object)
            else:
                return {'id': related_object.id, 'name': str(related_object)}

    def get_choice(self, field, value, flat=True):
        """
            get related object as {id:<> ,name:<>} or None of None
        """
        if value is None:
            return None
        else:
            choices = dict(field._get_choices())

            if flat:
                return str(choices[value])
            else:
                return {'id': value, 'name': str(choices[value])}

    def get_funding_organisations(self, measure):
        """
            returns funding organisation dict

        """

        return [{'id': obj.organization_id, 'percentage': obj.percentage, 'name': obj.organization.name}
                        for obj in measure.fundingorganization_set.all()]

    def get_object_for_api(self, measure, flat=True, include_related=False):
        """
            create object of measure
        """
        output = {
            'id':measure.id,
            'ident': measure.ident,
            'title': measure.title,
            'is_KRW_measure': measure.is_KRW_measure,
            'is_indicator': measure.is_indicator,
            'description': measure.description,
            'total_costs': measure.total_costs,
            'investment_costs': measure.investment_costs,
            'exploitation_costs': measure.exploitation_costs,
            'responsible_department': measure.responsible_department,
            'value': measure.value,
            'aggregation_type':  self.get_choice(Measure._meta.get_field('aggregation_type'), measure.aggregation_type, flat),
            'measure_type': self.get_related_object(measure.measure_type, flat),
            'period': self.get_related_object(measure.period, flat),
            'unit': self.get_related_object(measure.unit, flat),
            'categories': self.get_related_objects(measure.categories, flat),
            'initiator': self.get_related_object(measure.initiator, flat),
            'executive': self.get_related_object(measure.executive, flat),
            'areas': self.get_related_objects(measure.areas, flat),
            'waterbodies': self.get_related_objects(measure.waterbodies, flat),
            'funding_organizations': self.get_funding_organisations(measure),
            'read_only': measure.read_only,
            'import_raw': measure.import_raw,
            'import_source': measure.import_source,
        }
        return output


    def get(self, request):
        """
            returns object or list of objects

        """

        object_id = self.str2int_or_none(request.GET.get('object_id', None))
        include_related = self.str2bool_or_none(request.GET.get('include_related', False))
        flat = self.str2bool_or_none(request.GET.get('flat', True))

        print """input for api is:
                object_id: %s
                include_related: %s
                flat: %s
              """%(str(object_id), str(include_related), str(flat))
        
        if (object_id  is not None):
            #return single object
            measure = Measure.objects.get(id=object_id)
            output = self.get_object_for_api(measure, flat=flat, include_related=include_related)
            return {'success': True, 'data': output}

        else:
            #return list with objects
            start = int(request.GET.get('start', 0))
            limit = int(request.GET.get('limit', 25))

            output = []

            measures = Measure.objects.filter(deleted=False)
            for measure in measures[start:(start+limit)]:
                output.append(self.get_object_for_api(measure, flat=flat, include_related=include_related))

            return {'success': True, 'data': output, 'count': measures.count()}

    def post(self, request):
        """
            Update, create or delete records

        """
        action = request.GET.get('action', None)
        data = json.loads(self.CONTENT.get('data', []))
        edit_message = self.CONTENT.get('edit_message', None)

        print """input for api is:
                action: %s
                data: %s
                edit_message: %s
              """%(str(action), str(data), str(edit_message))

        output = None
        touched_objects = None
        
        if type(data) == dict:
            return_dict = True
            data = [data]
        else:
            return_dict = False

        if action == 'delete':
            success = self.delete_objects(
                data)
        elif action == 'create':
            success, touched_objects = self.create_objects(
                data)
        elif action == 'update':
            success, touched_objects = self.update_objects(
                data)
        else:
            logger.error("Unkown post action '%s'." % action)
            success = False

        if touched_objects:
            output = []
            for measure in touched_objects:
                output.append(self.get_object_for_api(measure, flat=False, include_related=True))

            if return_dict:
                #just return single object
                output = output[0]

        return {'success': success,
                'data': output}


    def save_single_many2many_relation(self, record, model_field, linked_records):
        """
            update specific part of manyToMany relations.
            input:
                - record: measure
                - model_field. many2many field object
                - linked_records. list with dictionaries with:
                    id: id of related objects
                    optional some relations in case the relation is through another object

        """


        model_link = getattr(record, model_field.name)
        existing_links = dict([(obj.id, obj) for obj in model_link.all()])

        for linked_record in linked_records:

            if existing_links.has_key(linked_record['id']):
                #update record
                link = existing_links[linked_record['id']]
                link.save()
                del existing_links[linked_record['id']]
            else:
                #create new
                model_link.add(
                    model_field.rel.to.objects.get(pk=linked_record['id']))

        #remove existing links, that are not anymore
        for link in existing_links.itervalues():
            model_link.remove(link)

    def update_many2many(self, record, model_field, linked_records):
        """
            update specific part of manyToMany relations.
            input:
                - record: measure
                - model_field. many2many field object
                - linked_records. list with dictionaries with:
                    id: id of related objects
                    optional some relations in case the relation is through another object

        """

        if model_field.name == 'funding_organizations':
            print 'funding_organizations'
            record.set_fundingorganizations(linked_records)
        else:
            #areas, waterbodies, category
            self.save_single_many2many_relation(record, model_field, linked_records)


    def update_objects(self, data):
        """
            Update records

            issues(todo):
            - everything in one databasetransaction
        """
        touched_objects = []
        model = Measure

        success = True

        for item in data:
            record = model.objects.get(pk=item['id'])
            touched_objects.append(record)

            for (key, value) in item.items():
                key = str(key)
                #value = str(value)
#                if value == "" or value == "None":
#                    continue
                try:
                    model_field = model._meta.get_field(key)

                    if model_field.rel is not None and type(model_field.rel) == models.ManyToManyRel:
                        self.update_many2many(record, model_field, value)
                    else:
                        if type(model_field.rel) == models.ManyToOneRel:
                            #input is a dictionary with an id and name in json
                            if value is None or value == {} or value == []:
                                value = None
                            else:
                                if type(value) == list:
                                    value = value[0]
                                value = model_field.rel.to.objects.get(pk=value['id'])

                        if type(model_field) == models.IntegerField and len(model_field._get_choices()) > 0:
                            #input is a dictionary with an id and name in json
                            if value is None or value == {} or value == []:
                                value = None
                            else:
                                if type(value) == list:
                                    value = value[0]
                                value = value['id']

                        if isinstance(model_field, models.IntegerField):
                            value = self.str2int_or_none(value)
                        setattr(record, key, value)

                        if isinstance(model_field, models.FloatField):
                            value = self.str2float_or_none(value)
                        setattr(record, key, value)

                        if isinstance(model_field, models.BooleanField):
                            value = self.str2bool_or_none(value)
                            print value
                        setattr(record, key, value)

                except FieldDoesNotExist:
                    logger.error("Field %s.%s not exists." % (
                            model._meta.module_name, key))
                    success = False
                    Exception('field error')

                record.save()
        return success, touched_objects

    def delete_objects(self, data):
        """Deactivate measure objects."""
        success = True

        model = Measure

        try:
            for record in data:
                object_id = record['id']
                object = model.objects.filter(
                    pk=object_id)
                if not object.exists():
                    continue
                object = object[0]
                object.deleted = True
                object.save()
        except:
                success = False
        return success