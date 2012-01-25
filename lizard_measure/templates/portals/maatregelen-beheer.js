{% load get_grid %}
{% load get_portal_template %}

{% if perms.auth.is_analyst %}

{
    itemId: 'maatregelen-beheer',
    title: 'maatregelen-beheer',
	xtype: 'portalpanel',
    breadcrumbs: [
        {
            name: 'maatregelen-beheer'
        }
    ],
	items:[{
		flex:1,
		items: [{
            title: 'Maatregelen',
            anchor:'100%',
            flex:1,
            xtype: 'leditgrid',
            columnLines: true,


            plugins: [
                'applycontext'
            ],
            applyParams: function(params) {
                var params = params|| {};
                console.log('apply params');
                console.log(params);

                if (this.store) {
                    //this.store.applyParams({object_id: params.object_id,
                    //                        area_object_type: 'Structure'});
                    this.store.load();
                }
            },
            //proxyUrl: '/portal/wbstructures.json',
            proxyUrl: '/measure/api/measure/',
            proxyParams: {
                flat: false,
                size: 'small',
                include_geom: false
            },
            addEditIcon: true,
            addDeleteIcon: true,
            actionEditIcon:function(record) {
                console.log('edit record:');
                console.log(record);

                Ext.create('Ext.window.Window', {
                    title: 'Maatregel',
                    width: 800,
                    height: '60%',
                    editpopup: true,
                    //autoScroll: true,
                    loader:{
                        loadMask: true,
                        autoLoad: true,
                        url: '/measure/measure_detailedit_portal/',
                        ajaxOptions: {
                            method: 'GET'
                        },
                        params: {
                            measure_id: record.data.id
                        },
                        renderer: 'component'
                    }
                }).show();
            },
            dataConfig:[
                //is_computed altijd 1 in en 1 uit en verder niet
                {name: 'id', title: 'id', editable: false, visible: false, width: 30, type: 'number'},
                {name: 'ident', title: 'ident', editable: false, visible: false, width: 100, type: 'text'},
                {name: 'title', title: 'titel', editable: true, visible: true, width: 200, type: 'text'},
                {name: 'is_KRW_measure', title: 'KRW maatregel', editable: true, visible: true, width: 100, type: 'boolean'},//automatisch aanmaken
                {name: 'is_indicator', title: 'focus maatregel', editable: true, visible: true, width: 100, type: 'boolean'},
                {name: 'parent', title: 'onderdeel van', editable: false, visible: true, width: 75, type: 'combo'},
                {name: 'measure_type', title: 'maatregeltype', editable: true, visible: true, width: 150, type: 'combo', choices: Ext.JSON.decode({% autoescape off %}'{{ measure_types }}'{% endautoescape %})},//todo: voeg choices to vanuit model
                {name: 'period', title: 'periode', editable: true, visible: true, width: 100, type: 'combo', choices: Ext.JSON.decode({% autoescape off %}'{{ periods }}'{% endautoescape %})},//todo: voeg choices to vanuit model
                {name: 'categories', title: 'categorie', editable: false, visible: true, width: 150, type: 'combo', multiSelect: true, choices: Ext.JSON.decode({% autoescape off %}'{{ categories }}'{% endautoescape %})},
                {name: 'value', title: 'waarde', editable: true, visible: true, width: 75, type: 'number'},
                {name: 'unit', title: 'eenheid', editable: true, visible: true, width: 75, type: 'combo', choices: Ext.JSON.decode({% autoescape off %}'{{ units }}'{% endautoescape %})},
                {name: 'initiator', title: 'initiatiefnemer', editable: true, visible: true, width: 100,
                    type: 'combo', remote: true, store: {
                        fields: ['id', 'name'],
                        proxy: {
                            type: 'ajax',
                            url: '/measure/api/organization/?_accept=application%2Fjson',
                            reader: {
                                type: 'json',
                                root: 'data'
                            }
                        }
                    }
                },
                {name: 'executive', title: 'uitvoerder', editable: true, visible: true, width: 100,
                    type: 'combo', remote: true, store: {
                        fields: ['id', 'name'],
                        proxy: {
                            type: 'ajax',
                            url: '/measure/api/organization/?_accept=application%2Fjson',
                            reader: {
                                type: 'json',
                                root: 'data'
                            }
                        }
                    }
                },
                {name: 'responsible_department', title: 'afdeling', editable: true, visible: true, width: 75, type: 'text'},

                {name: 'total_costs', title: 'totale kosten', editable: true, visible: true, width: 75, type: 'number'},
                {name: 'investment_costs', title: 'investeringskosten', editable: true, visible: true, width: 75, type: 'number'},
                {name: 'exploitation_costs', title: 'exploitatiekosten', editable: true, visible: true, width: 75, type: 'number'},

                {name: 'waterbodies', title: 'KRW waterlichamen', editable: false, visible: true, width: 100, type: 'gridcombobox'},
                {name: 'areas', title: 'Aan/ afvoergebieden', editable: false, visible: true, width: 100, type: 'gridcombobox'}
           ]
        }]
	}]
}
{% else %}
    {% get_portal_template geen_toegang %}
{% endif %}
