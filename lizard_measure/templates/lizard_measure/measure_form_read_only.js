{
    xtype: 'formautoload',
    layout: 'anchor',
    autoScroll: true,
    trackResetOnLoad: true,
    bodyPadding: '10 25 10 10',//padding on the right side 25 for scrollbar
    height: '100%',
    loadProxy: {
        url: '/history/api_object/{{view.log_entry_id}}',
        type: 'ajax',
        method: 'GET',
        reader: {
          root: 'data',
          type: 'json'
        },
        params: {
            _accept: 'application/json',
        },
        success: function(form, action) {
            console.log('success gives:');
            console.log(arguments);
        },
        failure: function(form, action) {
            Ext.Msg.alert("Load failed", action.result.errorMessage);
        }
    },
    items:[
        {
            name: 'id',
            xtype: 'hiddenfield'
        },
        {
            fieldLabel: 'Ident',
            name: 'ident',
            width: 200,
            xtype: 'textfield',
            allowBlank: false
        },
        {
            fieldLabel: 'Naam',
            name: 'title',
            anchor: '100%',
            xtype: 'textfield',
            allowBlank: false
        },
        {
            fieldLabel: 'Onderdeel van maatregel',
            name: 'parent',
            displayField: 'name',
            anchor: '100%',
            valueField: 'id',
            xtype: 'combodict',
            forceSelection: true,
            allowBlank: true,
            store: {
                fields: ['id', 'name'],
                data: 'parent'
            },
        },
{
            fieldLabel: 'KRW maatregel',
            name: 'is_KRW_measure',
            xtype: 'checkbox',
            inputValue: true,
            allowBlank: true
        },

        {
            fieldLabel: 'Focus maatregel',
            name: 'is_indicator',
            inputValue: true,
            xtype: 'checkbox',
            allowBlank: true
        },
        {
            fieldLabel: 'In SGBP',
            name: 'in_sgbp',
            inputValue: true,
            xtype: 'checkbox',
            allowBlank: true
        },
        {
            fieldLabel: 'Beschrijving',
            name: 'description',
            grow: true,
            anchor: '100%',
            xtype: 'textareafield',
            allowBlank: true
        },
        {
            fieldLabel: 'Maatregel type',
            name: 'measure_type',
            displayField: 'name',
            valueField: 'id',
            anchor: '100%',
            xtype: 'combodict',
            store: {
                fields: ['id', 'name'],
                data: 'measure_type'
            },
            multiSelect: false,
            forceSelection: true,
            allowBlank: false,
        },
        {
            fieldLabel: 'Waarde',
            name: 'value',
            xtype: 'numberfield',
            minValue: 0,
            allowBlank: false,
            width: 200
        },
        {
            fieldLabel: 'Eenheid',
            name: 'unit',
            displayField: 'name',
            valueField: 'id',
            xtype: 'combodict',
            store: {
                fields: ['id', 'name'],
                data: 'unit'
            },
            forceSelection: true,
            allowBlank: false,
            width: 200
        },
        {
            fieldLabel: 'Periode',
            name: 'period',
            displayField: 'name',
            valueField: 'id',
            xtype: 'combodict',
            store: {
                fields: ['id', 'name'],
                data: 'period'
            },
            forceSelection: true,
            allowBlank: false,
            width: 400
        },
        {
            fieldLabel: 'Beleidsdoelen',
            name: 'categories',
            displayField: 'name',
            valueField: 'id',
            xtype: 'combodict',
            store: {
                fields: ['id', 'name'],
                data: 'categories'
            },
            multiSelect: true,
            forceSelection: true,
            allowBlank: false,
            width: 400
        },
        {
            xtype: 'tablefield',
            fieldLabel: 'Effect op ESF',
            name: 'esflink_set',
            field_name: 'Effect',
            editable: true,
            extra_fields:[{
                text: 'is gericht op',
                dataIndex: 'is_target_esf',
                width:100,
                xtype: 'checkcolumn',
                field: {
                    xtype: 'checkbox'
                }
            },{
                text: 'verwacht positief effect',
                dataIndex: 'positive',
                width:150,
                xtype: 'checkcolumn',
                field: {
                    xtype: 'checkbox'
                }
            },{
                text: 'verwacht negatief effect',
                dataIndex: 'negative',
                width:150,
                xtype: 'checkcolumn',
                field: {
                    xtype: 'checkbox'
                }
            }]
        },
        {
            xtype:'fieldset',
            collapsible: true,
            title: 'Planning',
            collapsed: false,
            layout: 'anchor',
            defaults: {
                anchor: '100%'
            },
            items: [
            {
                xtype: 'tablefield',
                fieldLabel: 'planning en realisatie',
                name: 'status_moments',
                field_name: 'status',
                editable: true,
                extra_fields:[{
                    text: 'planning',
                    dataIndex: 'planning_date',
                    width:100,
                    xtype: 'datecolumn',
                    format:'d-m-Y',
                    field: {
                        xtype: 'datefield',
                        format: 'd-m-Y'
                    }
                },{
                    text: 'realisatie',
                    dataIndex: 'realisation_date',
                    width:100,
                    xtype: 'datecolumn',
                    format:'d-m-Y',
                    field: {
                        xtype: 'datefield',
                        format: 'd-m-Y'
                    }
                }]

            }
        ]
        },
        {
            xtype:'fieldset',
            collapsible: true,
            title: 'Organisaties en kosten',
            collapsed: false,
            layout: 'anchor',
            items: [
            {
                fieldLabel: 'Initiatiefnemer',
                name: 'initiator',
                displayField: 'name',
                valueField: 'id',
                xtype: 'combodict',
                queryMode: 'remote', //'local' 'remote
                typeAhead: true,
                minChars:0,
                forceSelection: true,
                width: 400,
                store: {
                    fields: ['id', 'name'],
                    data: 'initiator'
                },
            },
            {
                fieldLabel: 'Afdeling',
                name: 'responsible_department',
                xtype: 'textfield',
                width: 400,
                allowBlank: true
            },
            {
                xtype: 'combodict',
                fieldLabel: 'Uitvoerder',
                name: 'executive',
                displayField: 'name',
                valueField: 'id',
                forceSelection: true,
                queryMode: 'remote', //'local' 'remote
                typeAhead: true,
                minChars:0,
                width: 400,
                store: {
                    fields: ['id', 'name'],
                    data: 'executive'
                },
            },
            {
                fieldLabel: 'Totale kosten (incl. btw)',
                name: 'total_costs',
                minValue: 0,
                allowDecimals: false,
                width: 200,
                xtype: 'numberfield'
            },
            {
                fieldLabel: 'Investeringskosten (incl. btw)',
                name: 'investment_costs',
                minValue: 0,
                allowDecimals: false,
                width: 200,
                xtype: 'numberfield'
            },
            {
                fieldLabel: 'Exploitatiekosten (incl. btw)',
                name: 'exploitation_costs',
                minValue: 0,
                allowDecimals: false,
                width: 200,
                xtype: 'numberfield'
            },
            {
                fieldLabel: 'Grondkosten (incl. btw)',
                name: 'land_costs',
                minValue: 0,
                allowDecimals: false,
                width: 200,
                xtype: 'numberfield'
            },
            {
                xtype: 'combomultiselect',
                fieldLabel: 'Kosten verdeling organisaties',
                name: 'funding_organizations',
                read_at_once: true,
                editable: true,
                anchor: '100%',
                extra_fields:[{
                    text: 'percentage',
                    dataIndex: 'percentage',
                    width:100,
                    field: {
                        xtype:'numberfield',
                        step:1,
                        allowDecimals: false,
                        maxValue: 100,
                        minValue: 0
                    }
                },{
                    text: 'opmerking',
                    dataIndex: 'comment',
                    width:200,
                    field: {
                        xtype:'textfield'
                    }
                }],
                combo_store: {
                    fields: [
                        {name: 'id', mapping: 'id'},
                        {name: 'percentage', mapping: 'percentage', defaultValue: 0},
                        {name: 'name', mapping: 'name'},
                        {name: 'comment', mapping: 'comment'}
                    ],
                }
            }
        ]
        },
        {
            xtype:'fieldset',
            collapsible: true,
            title: 'Link naar aan/afvoergebied en/of KRW-waterlichaam',
            collapsed: false,
            layout: 'anchor',
            defaults: {
                anchor: '100%'
            },
            items :[
            {
                xtype: 'combomultiselect',
                fieldLabel: 'aan/ afvoer gebieden',
                name: 'areas',
                field_name: 'aan/ afvoer gebieden',
                read_at_once: false,
                combo_store: {
                    fields: [
                        {name: 'id', mapping: 'id' },
                        {name: 'name', mapping: 'name' }
                    ],
                }
            }, {
                xtype: 'combomultiselect',
                fieldLabel: 'KRW waterlichamen',
                name: 'waterbodies',
                field_name: 'KRW waterlichamen',
                read_at_once: false,
                combo_store: {
                    fields: [
                        {name: 'id', mapping: 'id' },
                        {name: 'name', mapping: 'name' }
                    ],
                }
            }]
        },
        {
            fieldLabel: 'Geometrie (EPSG:4362)',
            name: 'geom',
            grow: true,
            anchor: '100%',
            editable: false,
            xtype: 'textareafield',
            allowBlank: true
        },
        {
            xtype:'fieldset',
            collapsible:true,
            title: 'Metadata',
            collapsed: true,
            layout: 'anchor',
            defaults: {
                anchor: '100%'
            },
            items :[
            {
                fieldLabel: 'Alleen lezen',
                name: 'read_only',
                xtype: 'displayfield'

            },
            {
                fieldLabel: 'Bron',
                name: 'import_source',
                xtype: 'displayfield'
            },
            {
                fieldLabel: 'Ruwe data bron',
                name: 'import_raw',
                xtype: 'displayfield'
            }
            ]
        }
    ],
}
