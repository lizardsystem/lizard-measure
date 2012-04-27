{% load get_grid %}
{% load get_portal_template %}
{
    itemId: 'stuurparameter-overzicht',
    title: 'stuurparameter-overzicht',
	xtype: 'portalpanel',
    breadcrumbs: [
        {
            name: 'stuurparameter-overzicht'
        }
    ],
	items:[{
		flex:1,
		items: [{
            title: 'Stuurparameters',
            anchor:'100%',
            flex:1,
            xtype: 'leditgrid',
            columnLines: true,
            store: {
                fields: ['id','name','code','test'],
                remoteSort: false,
                proxy: {
                    type: 'ajax',
                    url:'/measure/api/steer_parameter_overview/',
                    reader: {
                        type: 'json',
                        root: 'data'
                    }
                }
            },



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
            addEditIcon: true,
            addDeleteIcon: false,
            proxyUrl: '/measure/api/steer_parameter_overview/',
            proxyParams: {
                flat: false,
                size: 'small',
                include_geom: false
            },
            editable: false,
            usePagination: false,
            actionEditIcon:function(record) {
                var me = this

                Ext.create('Ext.window.Window', {
                    title: 'Stuurparameters instellen',
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
                        model: true,
                        url: '/measure/steering_parameter_form/',
                        params: {
                            object_id: record.get('code')
                        },
                        ajaxOptions: {
                            method: 'GET'
                        },
                        renderer: 'component'
                    }
                }).show();
           },
            dataConfig:[
                //is_computed altijd 1 in en 1 uit en verder niet
                {name: 'code', title: 'code', editable: false, visible: true, width: 80, type: 'text'},
                {name: 'name', title: 'gebiedsnaam', editable: false, visible: true, width: 200, type: 'text'},
                {% for graph in predefined_graphs %}
                    {name: 'st_{{ graph }}', title: '{{ graph }}', editable: false, visible: true, width: 80, type: 'text'},
                {% endfor %}
                {% for graph in parameters %}
                    {name: 'stf_{{ graph.no_point }}', title: '{{ graph.org }}', editable: false, visible: true, width: 80, type: 'text'},
                {% endfor %}
                {name: 'id', title: 'id', editable: false, visible: false, width: 200, type: 'text'}
           ]
        }]
	}]
}
