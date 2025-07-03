from django.utils.safestring import mark_safe

def form_builder(form_data):
    base_form_class = form_data['meta']['parent']
    form_name = form_data['meta']['name']
    
    class Meta:
        if 'model' in form_data['meta']:
            model = form_data['meta']['model']
        fields = [field['id'] for field in form_data['fields']]
        widgets = {
            field['id']: field['type'](attrs={'placeholder': field['placeholder']})
            for field in form_data['fields'] if type(field['type']) != list
        }
        
    form_class = type(form_name, (base_form_class,), {'Meta': Meta})

    def __init__(self, *args, **kwargs):
        super(form_class, self).__init__(*args, **kwargs)
        for index, field in enumerate(form_data['fields']):
            field_id = field['id']
            print(self.fields)
            self.fields[field_id].label = field['label']
            self.fields[field_id].help_text = ''
            if 'required' in field and field['required']:
                self.fields[field_id].required = True
            if isinstance(field['type'], list) and field['type']:
                model_class = field['type'][0]
                self.fields[field_id].queryset = model_class.objects.all()
                self.fields[field_id].empty_label = None
    form_class.__init__ = __init__
    
    def as_custom(self):
        """Переопределяем метод для рендеринга формы с использованием <div class="form-group">"""
        output = []
        for field in self:
            output.append(f'<div class="form-group">{field.label_tag()} {field}</div>')
        return mark_safe('\n'.join(output))

    form_class.as_custom = as_custom

    form_class.title = form_data['form']['page_title']
    form_class.form_name = form_data['form']['form_title']
    form_class.btn_confirm = form_data['form']['btn_confirm']
    form_class.sub_btn_link = form_data['form']['sub_btn_link']
    form_class.sub_btn_link_text = form_data['form']['sub_btn_link_text']

    return form_class