import json
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from django.db.models import DateField
from django.db.models.functions import Cast
from django.db import transaction

from apps.application.models import Application, ApplicationStatus, ApplicationStatusLog
from apps.api.serializers.applications import (
    ApplicationCreateSerializer,
    ApplicationSerializer,
    ApplicationNoFieldsSerializer,
    ApplicationStatusListSerializer,
    ApplicationStatusUpdateSerializer,
    ApplicationUpdateSerializer,
)
from apps.users.models import EventSubscriber
from apps.api.cache_tools.application_cache import (
    invalidate_application_caches,
    application_cache,
)


def set_event_response(event, other, response):
    now = timezone.now()
    response_text = (
        None if response is None else json.dumps(response, ensure_ascii=False)
    )
    EventSubscriber.objects.filter(event=event, other=other).update(
        response=response_text, last_check=now
    )


def check_event_for_user(user, event, other):
    now = timezone.now()
    with transaction.atomic():
        obj = (
            EventSubscriber.objects.select_for_update()
            .filter(user=user, event=event, other=other)
            .first()
        )
        if not obj:
            EventSubscriber.objects.create(
                user=user, event=event, response=None, other=other, last_check=now
            )
            return None
        if obj.response in (None, ""):
            obj.last_check = now
            obj.save(update_fields=["last_check"])
            return None
        try:
            payload = json.loads(obj.response)
        except Exception:
            payload = None
        obj.response = None
        obj.last_check = now
        obj.save(update_fields=["response", "last_check"])
        return payload


def _serialize_full_application(app: Application):
    return ApplicationSerializer(app).data


def _status_payload(app: Application):
    return {
        "id": app.id,
        "status": app.status,
        "msg": app.msg,
        "executor": app.executor.fullname if getattr(app, "executor", None) else None,
        "form": app.form.label if getattr(app, "form", None) else None,
    }


def on_application_created(application: Application):
    dept_id = None
    if getattr(application, "form", None) and getattr(
        application.form, "department", None
    ):
        dept_id = application.form.department.id
    set_event_response(
        "application-appear", dept_id, _serialize_full_application(application)
    )


def on_application_status_changed(application: Application):
    user_id = application.user.id if getattr(application, "user", None) else None
    dept_id = None
    if getattr(application, "form", None) and getattr(
        application.form, "department", None
    ):
        dept_id = application.form.department.id
    payload = _status_payload(application)
    if user_id is not None:
        set_event_response("application-status-change-userboard", user_id, payload)
    set_event_response("application-status-change-moderboard", dept_id, payload)


class ApplicationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        dept = request.query_params.get("department")
        user = request.query_params.get("user")
        created_after = request.query_params.get("created_after")
        created_before = request.query_params.get("created_before")
        short = request.query_params.get("short") == "true"

        cache_parts = [
            "list",
            dept,
            created_after,
            created_before,
            user,
            "short" if short else "full",
        ]
        cached_data = application_cache.get(*cache_parts)
        if cached_data is not None:
            return Response(cached_data)

        qs = Application.objects.all().order_by("-date")

        if dept is not None:
            qs = qs.filter(form__department_id=dept)
        if user is not None:
            qs = qs.filter(user_id=user)

        after_date = parse_date(created_after) if created_after else None
        before_date = parse_date(created_before) if created_before else None

        if after_date:
            qs = qs.annotate(date_only=Cast("date", DateField())).filter(
                date_only__gte=after_date
            )
        if before_date:
            qs = qs.annotate(date_only=Cast("date", DateField())).filter(
                date_only__lte=before_date
            )

        serializer_class = (
            ApplicationNoFieldsSerializer if short else ApplicationSerializer
        )
        out = serializer_class(qs, many=True)

        application_cache.set(out.data, *cache_parts)

        return Response(out.data)

    def post(self, request, *args, **kwargs):
        serializer = ApplicationCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            app = serializer.save()
            invalidate_application_caches(app)
            on_application_created(app)
            out = ApplicationSerializer(app)
            return Response(out.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationRetrieveUpdateAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        cache_key = ["detail", id]
        cached_data = application_cache.get(*cache_key)
        if cached_data is not None:
            return Response(cached_data)
        app = get_object_or_404(Application, pk=id)
        out = ApplicationSerializer(app)
        application_cache.set(out.data, *cache_key)
        return Response(out.data)

    def patch(self, request, id, *args, **kwargs):
        app = get_object_or_404(Application, pk=id)
        old_status = app.status
        serializer = ApplicationUpdateSerializer(app, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            invalidate_application_caches(app)
            if old_status != app.status:
                on_application_status_changed(app)
                ApplicationStatusLog.objects.create(
                    status=app.status,
                    previous_status=old_status,
                    who=app.executor,
                    application=app,
                )
            out = ApplicationSerializer(app)
            return Response(out.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationStatusListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        items = [{"key": c.name, "label": c.label} for c in ApplicationStatus]
        out = ApplicationStatusListSerializer(items, many=True)
        return Response(out.data)


class ApplicationStatusUpdateAPIView(APIView):
    def patch(self, request, id, *args, **kwargs):
        app = get_object_or_404(Application, pk=id)
        old_status = app.status
        serializer = ApplicationStatusUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        app.status = serializer.validated_data["status"]
        app.save(update_fields=["status"])
        invalidate_application_caches(app)
        if old_status != app.status:
            on_application_status_changed(app)
        out = ApplicationSerializer(app)
        return Response(out.data)
