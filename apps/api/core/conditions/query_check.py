
def is_from_form(request):
    return request.content_type.startswith('application/x-www-form-urlencoded') or\
           request.content_type.startswith('multipart/form-data')

