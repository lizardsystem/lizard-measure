{% load get_grid %}
{% load get_portal_template %}

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
            read_only_field: 'read_only',
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
            enterEditSummary: false,
            proxyUrl: '/measure/api/organization/',
            proxyParams: {
                flat: false
            },
            {% if perm.is_funct_beheerder %}
            saveEdits: function() {
                var do_alert = false;
                Ext.each(this.store.getNewRecords(), function(record) {
                    var description = record.get('description');
                    if (description == undefined) {
                        do_alert = true;
                    } else if (description.length < 3) {
                        do_alert = true;
                    }
                });
                Ext.each(this.store.getUpdatedRecords(), function(record) {
                    var description = record.get('description');
                    if (description == undefined) {
                        do_alert = true;
                    } else if (description.length < 3) {
                        do_alert = true;
                    }
                });
                if (do_alert) {
                    Ext.Msg.alert('Invoer fout', 'De organisatie naam moet minimaal 3 tekens langs zijn.');
                } else {
                    this.store.sync();
                }
            },
    {% else %}
            useSaveBar: false,
                editable: false,
    {% endif %}
            dataConfig:[
                //is_computed altijd 1 in en 1 uit en verder niet
                {name: 'id', title: 'id', editable: false, visible: false, width: 30, type: 'number'},
                {name: 'code', title: 'code', editable: false, visible: true, width: 100, type: 'number'},
                {name: 'description', title: 'naam', editable: true, visible: true, width: 200, type: 'text'},
                {name: 'group', title: 'groep', editable: false, visible: true, width: 200, type: 'text'},
                {name: 'source', title: 'bron', editable: false, visible: true, width: 200, type: 'gridcombobox'},
                {name: 'read_only', title: 'Alleen lezen', editable: false, visible: true, width: 50, type: 'boolean'}
           ]
        }]
	}]
}

