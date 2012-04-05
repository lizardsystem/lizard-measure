
{
    layout: 'anchor',
    autoScroll: true,
    trackResetOnLoad: true,
    bodyPadding: '10 25 10 10',//padding on the right side 25 for scrollbar
    height: '100%',
    items:[{
        html: '<h1>{{ area.name }}</h1><br /><i>Aanwijzingen bij het toevoegen van enkelvoudige grafieken:</i><p>Vul in het veld "locaties" een of meer locaties in, gescheiden door een punt-komma.</p><p>Eventueel kunnen de locaties ook worden opgegeven in de vorm &lt;locatie_id,moduleinstance_id,timestep_id,qualifieriset_id&gt; om een specifieke tijdreeks te benaderen.</p><p>Een aantal voorbeelden:</p><div class="lizard"><table><tr><th>naam</th><th>volgorde</th><th>type</th><th>heeft doel</th><th>doel waarde</th><th>parameter code</th><th>locaties</th></tr><tr><td>Voorbeeld1</td><td>10</td><td>toestand</td><td>ja</td><td>1</td><td>chloride</td><td>3201</td></tr><tr><td>Voorbeeld2</td><td>20</td><td>evaluatie</td><td>ja</td><td>1</td><td>SO4</td><td>SAP010;HAP010</td></tr><tr><td>Voorbeeld3</td><td>30</td><td>evaluatie</td><td>nee</td><td>0</td><td>PO4.bodem</td><td>SAP010,Import_Reeksen,NETS</td></tr></table></div><br />'
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
            {name: 'location_modulinstance_string', title: 'locaties', editable: true, visible: true, width: 330, type: 'text'}
        ]
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
