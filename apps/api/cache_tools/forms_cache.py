from .helper import CacheHelper

forms_data_cache = CacheHelper("forms:data", ttl=3600)
forms_list_cache = CacheHelper("forms:list", ttl=3600)


def cache_key_for_form(form_id):
    return f"form:{form_id}"


def cache_key_for_forms_list(department_id=None, visible=False):
    if visible:
        return "forms:list:visible"
    if department_id is not None:
        return f"forms:list:department:{department_id}"
    return "forms:list:all"
