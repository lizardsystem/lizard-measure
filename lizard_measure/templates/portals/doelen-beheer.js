{% load get_grid %}
{% load get_portal_template %}

{% if perms.auth.is_analyst %}

{
    itemId: 'doelen-beheer',
    title: 'doelen-beheer',
	xtype: 'portalpanel',
    breadcrumbs: [
        {
            name: 'doelen-beheer'
        }
    ],
	items:[{
		flex:1,
		items: [{
            title: 'Doelen (allen bekijken)',
            anchor:'100%',
            flex:1,
            xtype: 'leditgrid',
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
            proxyUrl: '/measure/api/score/',
            proxyParams: {

            },
            dataConfig:[
                {name: 'id', title: 'id', editable: false, visible: false, width: 100, type: 'text'},
                {name: 'area', title: 'Gebied', editable: false, visible: true, width: 200, type: 'gridcombobox'},
                {name: 'measuring_rod', title: 'Maatlat', editable: false, visible: true, width: 200, type: 'gridcombobox'},
                {name: 'current_value', title: 'waarde', editable: false, visible: true, width: 45, type: 'number'},
                {name: 'target_2015', title: '2015', editable: true, visible: true, width: 45, type: 'number'},
                {name: 'target_2027', title: '2027', editable: true, visible: true, width: 45, type: 'number'},
                {name: 'gep', title: '2027', editable: true, visible: true, width: 45, type: 'number'},
                {name: 'mep', title: '2027', editable: true, visible: true, width: 45, type: 'number'},
                {name: 'limit_insufficient_moderate', title: 'matig', editable: true, visible: true, width: 45, type: 'number'},
                {name: 'limit_bad_insufficient', title: 'slecht', editable: true, visible: true, width: 45, type: 'number'}

           ]
        }]
	}]
}
{% else %}
    {% get_portal_template geen_toegang %}
{% endif %}
