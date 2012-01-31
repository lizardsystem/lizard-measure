{% load get_grid %}
{% load get_portal_template %}

{% if perms.auth.is_analyst %}

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

                Ext.create('Ext.window.Window', {
                    title: 'Stuurparameter',
                    width: 800,
                    height: 600,
                    modal: true,
                    finish_edit_function: function (updated_record) {
                        me.store.load();
                    },
                    editpopup: true,
                    loader:{
                        loadMask: true,
                        autoLoad: true,
                        url: '/measure/stuurparameter_detailedit_portal/',
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
                {name: 'name', title: 'name', editable: true, visible: true, width: 200, type: 'text'},
                {name: 'waterbodies', title: 'KRW waterlichamen', editable: false, visible: true, width: 100, type: 'gridcombobox'},
                {name: 'areas', title: 'Aan/ afvoergebieden', editable: false, visible: true, width: 100, type: 'gridcombobox'}
           ]
        }]
	}]
}
{% else %}
    {% get_portal_template geen_toegang %}
{% endif %}
