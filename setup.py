import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SOOD_applications.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa

from apps.users.models import Department, UserRole  # noqa
from apps.forms.models import (  # noqa
    Enum,
    EnumTag,
    FieldType,
    Form,
    FormField,
    Field,
    FieldCharSet,
)  # noqa
from apps.application.models import Application, ApplicationFormField  # noqa

from itertools import product  # noqa
import uuid  # noqa

import random  # noqa
from datetime import datetime, timedelta  # noqa
from django.utils import timezone  # noqa
from django.db import transaction  # noqa


def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username="toster").exists():
        print("Создание суперюзера...")
        User.objects.create_superuser(
            username="toster", password="imposter", email="toster@example.com"
        )

    super_user = User.objects.get(username="toster")
    super_user.fullname = "SUPERUSER"
    super_user.role = UserRole.ADMIN
    super_user.verified = True
    super_user.proxy = True
    super_user.save()
    print("Создан суперюзер: toster")


def create_deps():
    print("-- Создание отделов")
    prog_dep, c = Department.objects.get_or_create(name="Отдел программирования")
    rem_dep, c = Department.objects.get_or_create(name="Отдел сетевой поддержки")
    print("Отделы созданы")
    return rem_dep, prog_dep


def get_users_deps_product(deps):
    print("-- Генерация сочетаний")
    users = [UserRole.USER, UserRole.MODERATOR, UserRole.ADMIN]
    combos = [p for p in product(deps, users) for _ in range(3)]
    print(f"Сгенерировано сочетаний: {len(combos)}")
    return combos


def create_users(users_deps):
    print("-- Создание пользователей")
    User = get_user_model()
    users = []

    for i, us in enumerate(users_deps):
        user = User(
            username=str(i),
            fullname=str(i),
            department=us[0],
            role=us[1],
            verified=bool(i % 2),
            proxy=i > 3,
        )
        user.set_password(str(i))
        users.append(user)

    created_users = User.objects.bulk_create(users)

    for user in created_users:
        print(f"Создан пользователь: {user.username}")

    return created_users


def create_enum_tags(rem_dep, prog_dep):
    print("-- Создание тэгов перечислений")
    tag1, c = EnumTag.objects.get_or_create(
        name="Принтер", department=rem_dep, shared=True
    )
    tag2, c = EnumTag.objects.get_or_create(name="Блюда")
    tag3, c = EnumTag.objects.get_or_create(name="Компьютеры", department=prog_dep)
    print("Тэги перечислений созданы")
    return tag1, tag2, tag3


def create_enums(tag1, tag2, tag3):
    print("-- Создание элементов перечислений")
    Enum.objects.get_or_create(value="Принтер п-1", enum_tag=tag1)
    Enum.objects.get_or_create(value="Принтер Lenovo", enum_tag=tag1)
    Enum.objects.get_or_create(value="Мьясо", enum_tag=tag2)
    Enum.objects.get_or_create(value="Пирожки с пирожками", enum_tag=tag2)
    Enum.objects.get_or_create(value="OIDI-123", enum_tag=tag3)
    Enum.objects.get_or_create(value="UZI-1", enum_tag=tag3)
    Enum.objects.get_or_create(value="UZI-2", enum_tag=tag3)
    Enum.objects.get_or_create(value="kpo-866", enum_tag=tag3)
    print("Элементы перечислений созданы")


def create_field_types():
    print("-- Создание типов полей")
    type_names = [
        ("text", "Строка"),
        ("textarea", "Текст"),
        ("number", "Число", "number"),
        ("date", "Дата"),
        ("time", "Время"),
        ("datetime", "Дата и время"),
        ("month", "Месяц"),
        ("week", "Неделя"),
        ("checkbox", "Чекбокс"),
        ("enum", "Перечисление", "enum"),
        ("charset", "Набор символов", "charset"),
    ]
    types = {
        tn[0]: FieldType.objects.get_or_create(
            name=tn[0], label=tn[1], type="" if len(tn) == 2 else tn[2]
        )[0]
        for tn in type_names
    }
    print(f"Типов полей создано/получено: {len(types)}")
    return types


def create_form(dep, name):
    new_form, c = Form.objects.get_or_create(
        department=dep,
        label=name,
        visible=True,
    )
    print(f"Форма создана: {name}")
    return new_form


def create_forms(rem_dep, prog_dep):
    print("-- Создание форм")
    f1 = create_form(rem_dep, "Testovaya Forma")
    f2 = create_form(rem_dep, "TTT")
    f3 = create_form(prog_dep, "Заявка на установку ПО")
    print("Формы созданы")
    return f1, f2, f3


def create_default_charsets(*deps):
    print("-- Создание стандартных наборов символов для полей")
    with transaction.atomic():
        digits, _ = FieldCharSet.objects.get_or_create(
            label="digits",
            defaults={
                "digits": True,
                "department": deps[0],
                "visible": True,
                "included": ".",
            },
        )

        latin_plus_digits, _ = FieldCharSet.objects.get_or_create(
            label="latin_plus_digits",
            defaults={
                "latin_lower": True,
                "latin_upper": True,
                "digits": True,
                "visible": True,
                "shared": True,
                "department": deps[1],
            },
        )

        cyrillic_full, _ = FieldCharSet.objects.get_or_create(
            label="cyrillic_full",
            defaults={
                "cyrillic_lower": True,
                "cyrillic_upper": True,
                "visible": True,
                "department": deps[1],
            },
        )

    return {
        "digits": digits,
        "latin_plus_digits": latin_plus_digits,
        "cyrillic_full": cyrillic_full,
    }


def create_field_examples(types, tag1, tag2, tag3, charset):
    print("-- Создание примеров полей")
    fields = [
        {"label": "Технологические пирожки", "type": types["enum"], "tag": tag2},
        {"label": "Количество", "type": types["number"]},
        {"label": "Компьютер", "type": types["enum"], "tag": tag3},
        {"label": "Стоимость", "type": types["number"], "decimals": 2},
        {"label": "Цена", "type": types["number"], "decimals": 2},
        {"label": "Описание", "type": types["textarea"]},
        {"label": "Принтер", "type": types["enum"], "tag": tag1},
        {"label": "Новое количество", "type": types["number"]},
        {"label": "Наименование", "type": types["text"]},
        {"label": "Ценник", "type": types["charset"], "charset": charset},
        {"label": "Дата 1", "type": types["date"]},
        {"label": "Время 1", "type": types["time"]},
        {"label": "Дата и время 1", "type": types["datetime"]},
        {"label": "Месяц 1", "type": types["month"]},
        {"label": "Неделя 1", "type": types["week"]},
        {"label": "Чекбокс 1", "type": types["checkbox"]},
    ]
    print(f"Примеров полей: {len(fields)}")
    return fields


def link_fields_to_forms(deps, forms, fields):
    ff1_list = []
    ff3_list = []
    for i, f in enumerate(fields):
        field, c = Field.objects.get_or_create(**f, department=deps[i % 2])
        ff, c = FormField.objects.get_or_create(form=forms[i % 3], field=field)
        if i % 3 == 0:
            ff1_list.append(ff)
        if i % 3 == 2:
            ff3_list.append(ff)
        print(f"Поле привязано: {field.label} -> форма {forms[i % 3].label}")
    print("Привязка полей к формам завершена")
    return ff1_list, ff3_list


def bulk_create_applications(
    count=10000,
    start_date_str=None,
    min_step_minutes=30,
    max_step_minutes=60,
    min_fields=1,
    max_fields=3,
):
    if start_date_str:
        start_dt = datetime.fromisoformat(start_date_str)
        base_dt = timezone.make_aware(start_dt, timezone.get_default_timezone())
    else:
        base_dt = timezone.now()
    users = list(get_user_model().objects.all())
    form = Form.objects.first()
    form_fields = list(FormField.objects.filter(form=form))
    current_dt = base_dt
    batch_size = 500
    to_create = []
    marker_to_date = {}
    created_ids = []
    total_created = 0
    print(
        f"-- Начало массового создания заявок: {count}, старт = {base_dt.isoformat()}"
    )
    for i in range(count):
        user = random.choice(users)
        app_dt = current_dt
        marker = str(uuid.uuid4())
        app = Application(
            form=form, user=user, date=app_dt, last_status_change=app_dt, msg=marker
        )
        to_create.append(app)
        marker_to_date[marker] = app_dt
        if len(to_create) >= batch_size:
            Application.objects.bulk_create(to_create, batch_size=batch_size)
            markers = [m for m in marker_to_date.keys() if m][-len(to_create) :]
            created = list(
                Application.objects.filter(msg__in=markers).values_list("id", "msg")
            )
            created_ids.extend([c[0] for c in created])
            for cid, cm in created:
                dt = marker_to_date.get(cm)
                if dt:
                    Application.objects.filter(id=cid).update(
                        date=dt, last_status_change=dt, msg=""
                    )
            total_created += len(to_create)
            print(
                f"Пакет создан: {total_created}/{count} заявок (последняя дата в пакете {app_dt.isoformat()})"
            )
            to_create = []
        step = random.randint(min_step_minutes, max_step_minutes)
        current_dt -= timedelta(minutes=step)
    if to_create:
        Application.objects.bulk_create(to_create, batch_size=batch_size)
        markers = [m for m in marker_to_date.keys() if m][-len(to_create) :]
        created = list(
            Application.objects.filter(msg__in=markers).values_list("id", "msg")
        )
        created_ids.extend([c[0] for c in created])
        for cid, cm in created:
            dt = marker_to_date.get(cm)
            if dt:
                Application.objects.filter(id=cid).update(
                    date=dt, last_status_change=dt, msg=""
                )
        total_created += len(to_create)
        print(
            f"Пакет создан: {total_created}/{count} заявок (последняя дата в пакете {app_dt.isoformat()})"
        )
    created_ids = created_ids[::-1]
    app_qs = Application.objects.filter(pk__in=created_ids).order_by("id")
    total_aff = 0
    print("-- Начало создания полей для заявок")
    with transaction.atomic():
        for idx, app in enumerate(app_qs, 1):
            num_fields = random.randint(min_fields, max_fields)
            chosen_ff = random.sample(form_fields, min(num_fields, len(form_fields)))
            aff_objs = [
                ApplicationFormField(
                    application=app, form_field=ff, value=str(random.randint(1, 100))
                )
                for ff in chosen_ff
            ]
            ApplicationFormField.objects.bulk_create(aff_objs)
            total_aff += len(aff_objs)
            if idx % 1000 == 0 or idx == len(created_ids):
                print(f"Обработано заявок для полей: {idx}/{len(created_ids)}")
    print(f"Создано заявок: {len(created_ids)}")
    print(f"Создано полей в заявках: {total_aff}")


def on_test_setup(apps_10000=False):
    deps = create_deps()

    users_deps = get_users_deps_product(deps)
    users = create_users(users_deps)  # noqa

    tag1, tag2, tag3 = create_enum_tags(*deps)
    create_enums(tag1, tag2, tag3)

    types = create_field_types()

    forms = create_forms(*deps)

    charset = create_default_charsets(*deps)

    fields = create_field_examples(types, tag1, tag2, tag3, charset["digits"])

    link_fields_to_forms(deps, forms, fields)

    if apps_10000:
        bulk_create_applications(10000)

    from django.core.cache import cache

    cache.clear()

    print("База данных заполнена начальными данными!")


if __name__ == "__main__":
    on_test_setup()
