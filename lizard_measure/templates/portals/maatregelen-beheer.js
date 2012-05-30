{% load get_grid %}
{% load get_portal_template %}


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
                console.log('apply params on store:');
                console.log(params);

                if (this.store) {
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
            addDeleteIcon: false,
            msgDeleteSelectedRecord: 'U verwijdert een maatregel. Weet U het zeker? U moet nog wel de wijzigingen opslaan om de maatregel werkelijk te verwijderen.',  // New feature of EditableGrid
            actionEditIcon:function(record) {
                var me = this
                console.log(this.store.getNewRecords())
                if (this.store.getNewRecords().length >0 ||
                    this.store.getUpdatedRecords().length >0 ||
                    this.store.getRemovedRecords().length >0) {

                    Ext.Msg.alert("Let op", 'Sla eerst de bewerking(en) in het grid op, voordat een enkel record kan worden bewerkt');
                    return
                }

                console.log('edit record:');
                console.log(record);

                if (record) {
                    params = {
                        measure_id: record.data.id
                    }

                } else {
                    params = null
                }

                Ext.create('Ext.window.Window', {
                    title: 'Maatregel',
                    width: 800,
                    height: 600,
                    modal: true,
                    constrainHeader: true,
                    finish_edit_function: function (updated_record) {
                        me.store.load();
                    },
                    editpopup: true,
                    loader:{
                        loadMask: true,
                        autoLoad: true,
                        url: '/measure/measure_detailedit_portal/',
                        ajaxOptions: {
                            method: 'GET'
                        },
                        params: params,
                        renderer: 'component'
                    }
                }).show();
            },
            addRecord: function() {
                this.actionEditIcon();
           },
            dataConfig:[
                //is_computed altijd 1 in en 1 uit en verder niet
                {name: 'id', title: 'id', editable: false, visible: false, width: 30, type: 'number'},
                {name: 'ident', title: 'ident', editable: false, visible: false, width: 100, type: 'text'},
                {name: 'title', title: 'titel', editable: false, visible: true, width: 200, type: 'text'},
                {name: 'waterbodies', title: 'KRW waterlichamen', editable: false, sortable: false, visible: true, width: 200, type: 'gridcombobox'},
                {name: 'areas', title: 'Aan/ afvoergebieden', editable: false, sortable: false, visible: true, width: 200, type: 'gridcombobox'},
                {name: 'import_source', title: 'bron', editable: false, sortable: false, visible: true, width: 100, type: 'text'},
                {name: 'status_planned', title: 'planning', editable: false, visible: true, sortable: false, width: 100, type: 'text'},
                {name: 'status_realisation', title: 'realisatie', editable: false, sortable: false, visible: true, width: 100, type: 'text'},
                {name: 'is_KRW_measure', title: 'KRW maatregel', editable: true, visible: true, width: 100, type: 'boolean'},//automatisch aanmaken
                {name: 'is_indicator', title: 'focus maatregel', editable: true, visible: true, width: 100, type: 'boolean'},
                {name: 'parent', title: 'onderdeel van', editable: false, visible: true, width: 75, type: 'combo'},
                {name: 'measure_type', title: 'maatregeltype', editable: true, visible: true, width: 150, type: 'combo', choices: Ext.JSON.decode({% autoescape off %}'{{ measure_types }}'{% endautoescape %})},//todo: voeg choices to vanuit model
                {name: 'period', title: 'periode', editable: true, visible: true, width: 100, type: 'combo', choices: Ext.JSON.decode({% autoescape off %}'{{ periods }}'{% endautoescape %})},//todo: voeg choices to vanuit model
                {name: 'categories', title: 'beleidsdoel', editable: false, visible: true, sortable: false, width: 150, type: 'combo', multiSelect: true, choices: Ext.JSON.decode({% autoescape off %}'{{ categories }}'{% endautoescape %})},
                {name: 'value', title: 'waarde', editable: true, visible: true, width: 75, type: 'number'},
                {name: 'unit', title: 'eenheid', editable: true, visible: true, width: 75, type: 'combo', choices: Ext.JSON.decode({% autoescape off %}'{{ units }}'{% endautoescape %})},
                {name: 'initiator', title: 'initiatiefnemer', editable: true, visible: true, width: 100,
                    type: 'combo', remote: true, store: {
                        fields: ['id', 'name'],
                        proxy: {
                            type: 'ajax',
                            url: '/measure/api/organization/?_accept=application%2Fjson&size=id_name',
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
                            url: '/measure/api/organization/?_accept=application%2Fjson&size=id_name',
                            reader: {
                                type: 'json',
                                root: 'data'
                            }
                        }
                    }
                },
                {name: 'responsible_department', title: 'afdeling', editable: true, visible: true, width: 75, type: 'text'},

                {name: 'total_costs', title: 'totale kosten', editable: true, sortable: false, visible: true, width: 75, type: 'number'},
                {name: 'investment_costs', title: 'investeringskosten', editable: true, visible: true, width: 75, type: 'number'},
                {name: 'exploitation_costs', title: 'exploitatiekosten', editable: true, visible: true, width: 75, type: 'number'},
                {name: 'land_costs', title: 'grondkosten', editable: true, visible: true, width: 75, type: 'number'},
                {name: 'target_esf', title: 'Doel ESF', editable: false, sortable: false, visible: true, width: 100, type: 'text'},
                {name: 'effect_esf', title: 'Effect op ESF', editable: false, sortable: false, visible: true, width: 100, type: 'text'}
           ]
        }]
	}]
}

