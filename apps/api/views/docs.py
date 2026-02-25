import os
from django.http import Http404, FileResponse, HttpResponseForbidden
from django.utils.http import http_date
from rest_framework.views import APIView, settings


FILES_DIR = os.path.join(settings.BASE_DIR, "files")


def build_mapping(dir_name, items, ext=".docx"):
    if dir_name:
        prefix = dir_name.rstrip("/\\") + os.sep
    else:
        prefix = ""
    mapping = {}
    if isinstance(items, dict):
        for key, fname in items.items():
            mapping[key] = prefix + fname + ext
        return mapping
    for it in items:
        if isinstance(it, (list, tuple)) and len(it) == 2:
            key, fname = it
        else:
            key = it
            fname = it
        mapping[key] = prefix + fname + ext
    return mapping


FILE_MAPPING_OTHER = build_mapping(
    "", {"register_login": "Вход и регистрация", "termins": "Словарь терминов"}
)
FILE_MAPPING_USER = build_mapping("Пользователю", {"create_app": "Создание заявки"})
FILE_MAPPING_MODERATOR = build_mapping(
    "Исполнителю", {"process_app": "Обработка заявки"}
)
FILE_MAPPING_ADMIN = build_mapping(
    "Руководителю",
    {
        "charsets": "Управление наборами символов",
        "enums": "Управление перечислениями",
        "users": "Управление сотрудниками",
        "forms": "Управление формами",
        "fields": "Управление шаблонами полей",
        "report": "Формирование отчёта и пояснение результатов",
    },
)


class DocServeBase(APIView):
    def get_file_response(self, key, mapping):
        if key not in mapping:
            raise Http404("File key not found")
        rel_path = mapping[key]
        filepath = os.path.join(FILES_DIR, rel_path)
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            raise Http404("File not found")
        lower = filepath.lower()
        if not (lower.endswith(".doc") or lower.endswith(".docx")):
            return HttpResponseForbidden("Not a Word document")
        f = open(filepath, "rb")
        response = FileResponse(
            f, as_attachment=True, filename=os.path.basename(filepath)
        )
        response["Last-Modified"] = http_date(os.path.getmtime(filepath))
        return response


class DocOtherView(DocServeBase):
    def get(self, request, key, format=None):
        return self.get_file_response(key, FILE_MAPPING_OTHER)


# @permissions("r: user")
class DocUserView(DocServeBase):
    def get(self, request, key, format=None):
        return self.get_file_response(key, FILE_MAPPING_USER)


# @permissions("r: moderator")
class DocModeratorView(DocServeBase):
    def get(self, request, key, format=None):
        return self.get_file_response(key, FILE_MAPPING_MODERATOR)


# @permissions("r: admin")
class DocAdminView(DocServeBase):
    def get(self, request, key, format=None):
        return self.get_file_response(key, FILE_MAPPING_ADMIN)
