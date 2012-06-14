{% load get_grid %}
{% load get_portal_template %}


{
    itemId: 'esfpattern-beheer',
    title: 'Geschikte maatregelen conditie beheer',
	xtype: 'portalpanel',
    breadcrumbs: [
        {
            name: 'geschikte maatregelen-beheer'
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
            read_only_field: 'read_only',
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
            proxyUrl: '/measure/api/esf_pattern/',
            proxyParams: {
                flat: false,
                size: 'small',
                include_geom: false
            },
            editable: false,

            usePagination: false,
            {% if perm.is_funct_beheerder %}
                editable: true,
                useSaveBar: true,
                addEditIcon: true,
                addDeleteIcon: true,
                //read_only_field: 'read_only',
                actionEditIcon: function(record) {
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
                            esfpattern_id: record.data.id
                        }

                    } else {
                        params = null
                    }

                    Ext.create('Ext.window.Window', {
                        title: 'Geschikte maatregelen patroon',
                        width: 600,
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
                            url: '/measure/esf_pattern_form/',
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
            {% else %}
                useSaveBar: false,
            {% endif %}
            dataConfig:[
                {name: 'id', title: 'id', editable: false, visible: false, width: 30, type: 'number'},
                {name: 'pattern', title: 'ESF patroon', editable: false, visible: true, width: 110, type: 'gridcombobox'},
                {name: 'watertype_group', title: 'watertype groep', editable: false, visible: true, width: 110, type: 'gridcombobox'},
                {name: 'data_set', title: 'data_set', editable: false, visible: true, width: 110, type: 'gridcombobox'},
                {name: 'measure_types', title: 'maatregelen types', editable: false, visible: true, width:600, type: 'gridcombobox'},
                {name: 'read_only', title: 'read_only', editable: false, visible: false, width: 70, type: 'boolean'}
           ]
        }]
	}]
}

