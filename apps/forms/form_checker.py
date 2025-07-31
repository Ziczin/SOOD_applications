def check_and_set(attrs: list, attr: str):
    if not attr in attrs:
        attrs.append(attr)

def form_checker(data: dict):
    for field in data['fields']:
        field_type = field.get('type')
        if field_type is None: continue
        if type(field_type) in (list, set, tuple, frozenset):
            field['enum'] = [
                {'value': idx, 'text': name}
                for idx, name in enumerate(
                list(field_type[0].objects.order_by('id').values_list('name', flat=True)))]
            field['type'] = 'enum'
        if field.get('attrs') is None:
            field['attrs'] = ['required', ]
        else:
            check_and_set(field['attrs'], 'required')
    return data
