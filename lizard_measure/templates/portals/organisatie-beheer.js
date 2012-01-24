{% load get_grid %}
{% load get_portal_template %}

{% if perms.auth.is_analyst %}

{
    itemId: 'organisatie-beheer',
    title: 'organisatie-beheer',
	xtype: 'portalpanel',
    breadcrumbs: [
        {
            name: 'organisatie-beheer'
        }
    ],
	items:[{
		flex:1,
		items: [{
            title: 'Organisaties',
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
            proxyUrl: '/measure/api/organization/',
            proxyParams: {
                flat: false
            },
            dataConfig:[
                //is_computed altijd 1 in en 1 uit en verder niet
                {name: 'id', title: 'id', editable: false, visible: false, width: 30, type: 'number'},
                {name: 'ident', title: 'ident', editable: true, visible: true, width: 100, type: 'text'},
                {name: 'description', title: 'beschrijving', editable: true, visible: true, width: 200, type: 'text'},
                {name: 'group', title: 'groep', editable: true, visible: true, width: 200, type: 'text'},
                {name: 'source', title: 'bron', editable: false, visible: true, width: 200, type: 'gridcombobox'}
           ]
        }]
	}]
}
{% else %}
    {% get_portal_template geen_toegang %}
{% endif %}
