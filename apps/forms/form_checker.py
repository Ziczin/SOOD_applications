from django.db.models import F
from copy import deepcopy


def check_and_set(attrs: list, attr: str):
    if attr not in attrs:
        attrs.append(attr)


def form_checker(form_config: dict):
    data = deepcopy(form_config)
    for field in data["fields"]:
        field_type = field.get("type")
        if field_type is None:
            continue  # noqa
        if field_type == "enum":
            model = field["enum"]["model"]
            config = field["enum"]["config"]
            field["enum"] = list(
                model.objects.values(value=F(config["value"]), text=F(config["text"]))
            )
        if field.get("attrs") is None:
            field["attrs"] = [
                "required",
            ]
        else:
            check_and_set(field["attrs"], "required")
    return data
