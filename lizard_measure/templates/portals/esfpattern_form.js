
{
    xtype: 'formautoload',
    layout: 'anchor',
    autoScroll: true,
    trackResetOnLoad: true,
    bodyPadding: '10 25 10 10',//padding on the right side 25 for scrollbar
    height: '100%',
    url: '/measure/api/esf_pattern/?_accept=application/json&include_geom=true&action={% if pattern %}update{% else %}create{% endif %}',
{% if pattern %}
    loadProxy: {
        url: '/measure/api/esf_pattern/',
        type: 'ajax',
        method: 'GET',
        reader: {
          root: 'data',
          type: 'json'
        },
        params: {
            include_geom: true,
            flat: false,
            _accept: 'application/json',
            object_id: {{ pattern.id }}
        },
        success: function(form, action) {
            console.log('success gives:');
            console.log(arguments);
        },
        failure: function(form, action) {
            Ext.Msg.alert("Load failed", action.result.errorMessage);
        }
    },
{% endif %}
    items:[
        {
            name: 'id',
            xtype: 'hiddenfield'
        },
        {
            fieldLabel: 'ESF patroon',
            name: 'pattern',
            width: 200,
            xtype: 'textfield',
            allowBlank: false
        },

        {
            fieldLabel: 'Watertype groep',
            name: 'watertype_group',
            displayField: 'name',
            valueField: 'id',
            width: 400,
            xtype: 'combodict',
            store: {
                fields: ['id', 'name'],
                data: Ext.JSON.decode({% autoescape off %}'{{ watertype_group }}'{% endautoescape %})
            },
            multiSelect: false,
            forceSelection: true,
            allowBlank: false
        },
        {
            xtype: 'combomultiselect',
            fieldLabel: 'Maatregel types',
            name: 'measure_types',
            read_at_once: true,
            editable: true,
            anchor: '100%',
            combo_store: {
            fields: [
                {name: 'id', mapping: 'id'},
                {name: 'name', mapping: 'name'}
            ],
            proxy: {
                type: 'memory',
                data: Ext.JSON.decode({% autoescape off %}'{{ measure_types }}'{% endautoescape %})
            }
        }
    }],
    buttons:[
    {
        text: 'Annuleren',
        handler: function() {
            this.up('window').close();
        }
    },{
        text: 'Opslaan',
        //formBind: true, //only enabled once the form is valid
        //disabled: true,
        handler: function() {
            var form = this.up('form').getForm();
            var form_window = this.up('window')
            if (form.isValid()) {
                /* todo: de waarden zelf gaan rangschikken en verzenden */
                var values = form.getValues()

                if (!values['is_KRW_measure']) {
                    values['is_KRW_measure'] = false
                }
                if (!values['is_indicator']) {
                    values['is_indicator'] = false
                }


                Lizard.window.EditSummaryBox.show({
                    
                    fn: function (btn, text) {
                        if (btn=='ok') {
                            values.edit_summary = text;
                            form_window.setLoading(true);
                            Ext.Ajax.request({
                                url: '/measure/api/esf_pattern/?action={% if pattern %}update{% else %}create{% endif %}&_accept=application/json&flat=false',
                                params: {
                                    object_id: values.id,
                                    edit_message: text,
                                    data:  Ext.JSON.encode(values)
                                },
                                method: 'POST',
                                success: function(xhr) {
                                    Ext.Msg.alert("Opgeslagen", "Opslaan gelukt");
                                    form_window.close();
                                    form_window.setLoading(false);
                                    if (form_window.finish_edit_function) {
                                        form_window.finish_edit_function();
                                    }
                                },
                                failure: function(xhr) {
                                    Ext.Msg.alert("Fout", "Server communication error");
                                    form_window.setLoading(false);
                                }
                            });

                        }
                        return true;
                    }
                })
            }
        }
    }]
}