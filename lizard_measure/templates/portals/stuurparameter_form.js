
{
    layout: 'anchor',
    autoScroll: true,
    trackResetOnLoad: true,
    bodyPadding: '10 25 10 10',//padding on the right side 25 for scrollbar
    height: '100%',
    items:[{
        html: '<h1>{{ area.name }}</h1><br> '
    },{
        title: 'Enkelvoudige grafieken',
        anchor:'100%',
        autoHeight: true,
        xtype: 'leditgrid',
        useSaveBar: false,
        usePagination: false,
        storeAutoLoad: true,
        //proxyUrl: '/portal/wbbuckets.json',
        proxyUrl: '/measure/api/steer_free/',
        proxyParams: {
            filter: Ext.JSON.encode([{"property":"area","value":"{{ area.name }}"}])
        },
        dataConfig:[
            {name: 'id', title: 'id', editable: false, visible: false, width: 30, type: 'text'},//automatisch
            {name: 'area', title: 'gebied', editable: false, visible: false, only_store: true, width: 300, type: 'gridcombobox',
                defaultValue: {id:{{ area.id }}, name:'{{ area.name }}'}},//todo: hier gebieds info
            {name: 'name', title: 'naam', editable: true, visible: true, width: 100, type: 'text'},//automatisch genereren

            {name: 'order', title: 'volgorde', editable: true, visible: true, width: 50, type: 'number', defaultValue: 10},
            {name: 'for_evaluation', title: 'type', editable: true, visible: true, width: 70, type: 'gridcombobox',
                defaultValue: {id:false, name:'toestand'},
                choices: [{id:true, name:'evaluatie'},{id:false, name:'toestand'}]},//default invullen
            {name: 'has_target', title: 'heeft doel', editable: true, visible: true, width: 70, type: 'boolean'},
            {name: 'target_value', title: 'doel waarde', editable: true, visible: true, width: 70, type: 'float'},
            {name: 'parameter_code', title: 'parameter code', editable: true, visible: true, width: 100, type: 'text'},
            {name: 'location_modulinstance_string', title: 'locatie module instance, etc code', editable: true, visible: true, width: 330, type: 'text'}
        ]
    },{
        html: '<br><br>'
    },{
        title: 'Samengestelde grafieken',
  
        anchor:'100%',
        autoHeight: true,
        xtype: 'leditgrid',
        useSaveBar: false,
        usePagination: false,
        storeAutoLoad: true,
        proxyUrl: '/measure/api/steer_predefined/',
        proxyParams: {
            filter: Ext.JSON.encode([{"property":"area","value":"{{ area.name }}"}])
        },

        dataConfig:[
            {name: 'id', title: 'id', editable: false, visible: false, width: 30, type: 'text'},//automatisch
            {name: 'area', title: 'gebied', editable: false, visible: false, only_store: true, width: 300, type: 'gridcombobox',
                defaultValue: {id:{{ area.id }}, name:'{{ area.name }}'}},//todo: hier gebieds info
            {name: 'name', title: 'naam', editable: true, visible: true, width: 100, type: 'text'},//automatisch genereren
            {name: 'order', title: 'volgorde', editable: true, visible: true, width: 50, type: 'number'},
            {name: 'for_evaluation', title: 'type', editable: true, visible: true, width: 70, type: 'gridcombobox', choices: [{id:true, name:'evaluatie'},{id:false, name:'toestand'}],//default invullen
                defaultValue: {id:false, name:'toestand'},
                choices: [{id:true, name:'evaluatie'},{id:false, name:'toestand'}]},//default invullen
            {name: 'predefined_graph', title: 'grafiek', editable: true, visible: true, width: 100, type: 'gridcombobox',
                choices: Ext.JSON.decode('{% autoescape off %}{{ predefined_graphs }}{% endautoescape %}')},//default invullen
            {name: 'area_of_predefined_graph', title: 'gebied', editable: true, visible: true, width: 330,
                type: 'gridcombobox', choices: Ext.JSON.decode('{% autoescape off %}{{ related_areas }}{% endautoescape %}')}
       ]
    }],
    bbar:[
    {
        text: 'Annuleren',
        handler: function() {
            this.up('window').close();
        }
    },
    {
        xtype: 'button',
        text: 'Reset',
        iconCls: 'l-icon-cancel',
        handler: function (menuItem, checked) {
            var panel = menuItem.up('panel');
            var grids = panel.query('leditgrid');
            for (var i = 0; i < grids.length; i++) {
                grids[i].cancelEdits()
            }
        }
    },
    {
        xtype: 'button',
        text: 'Save',
        iconCls: 'l-icon-disk',
        handler: function (menuItem) {
            var panel = menuItem.up('panel');
            var grids = panel.query('leditgrid');
            panel_global = panel;
            for (var i = 0; i < grids.length; i++) {
                grids[i].saveEdits();
            }
        }
    }]
}