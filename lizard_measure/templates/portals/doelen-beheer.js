{% load get_grid %}
{% load get_portal_template %}


{
    itemId: 'doelen-beheer',
    title: 'doelen-beheer',
	xtype: 'portalpanel',
    breadcrumbs: [
        {
            name: 'EKR overzicht'
        }
    ],
	items:[{
		flex:1,
		items: [{
            title: 'Doelen (allen bekijken)',
            anchor:'100%',
            flex:1,
            xtype: 'leditgrid',
            editable: false,
            useSaveBar: false,
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
                test:'test'

            },
            dataConfig:[
                {name: 'id', title: 'id', editable: false, visible: false, width: 100, type: 'text'},
                {name: 'area', title: 'gebied', editable: false, visible: true, width: 200, type: 'gridcombobox'},
                {name: 'measuring_rod', title: 'maatlat', editable: false, visible: true, width: 200, type: 'gridcombobox'},
                {name: 'latest_value', title: 'waarde', editable: false, visible: true, width: 45, type: 'auto'},
                {name: 'latest_comment', title: 'oordeel', editable: false, visible: true, width: 75, type: 'auto'},
                {name: 'latest_timestamp', title: 'datum', editable: false, visible: true, width: 115, type: 'auto'},
                {name: 'target_2015', title: '2015', editable: true, visible: true, width: 45, type: 'auto'},
                {name: 'target_2027', title: '2027', editable: true, visible: true, width: 45, type: 'auto'},
                {name: 'mep', title: 'mep', editable: true, visible: true, width: 45, type: 'auto'},
                {name: 'gep', title: 'gep', editable: true, visible: true, width: 45, type: 'auto'},
                {name: 'limit_insufficient_moderate', title: 'matig', editable: true, visible: true, width: 45, type: 'auto'},
                {name: 'limit_bad_insufficient', title: 'slecht', editable: true, visible: true, width: 45, type: 'auto'}

           ]
        }]
	}]
}

