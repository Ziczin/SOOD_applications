import os
from django.conf import settings
from django.http import Http404, FileResponse, HttpResponseForbidden
from django.utils.http import http_date
from rest_framework.views import APIView

from apps.api.core.permissions import permissions

FILES_DIR = os.path.join(settings.BASE_DIR, "files")

FILE_MAPPING_USER = {
    "public_manual": "user_manual.docx",
    "terms": "terms.docx",
}

FILE_MAPPING_MODERATOR = {
    "mod_guideline": "mod_guideline.docx",
    "report_template": "report_template.docx",
}

FILE_MAPPING_ADMIN = {
    "staff_policy": "staff_policy.docx",
    "financial_report": "financial_report.docx",
}


def _abs_path_from_mapping(rel_path):
    return os.path.join(FILES_DIR, rel_path)


class DocServeBase(APIView):
    def get_file_response(self, key, mapping):
        if key not in mapping:
            raise Http404("File key not found")
        rel_path = mapping[key]
        filepath = _abs_path_from_mapping(rel_path)
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


@permissions("r: user")
class DocUserView(DocServeBase):
    def get(self, request, key, format=None):
        return self.get_file_response(key, FILE_MAPPING_USER)


@permissions("r: moderator")
class DocModeratorView(DocServeBase):
    def get(self, request, key, format=None):
        return self.get_file_response(key, FILE_MAPPING_MODERATOR)


@permissions("r: admin")
class DocAdminView(DocServeBase):
    def get(self, request, key, format=None):
        return self.get_file_response(key, FILE_MAPPING_ADMIN)
