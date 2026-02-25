from django.db import transaction
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from apps.users.models import EventSubscriber


def check_event(user_id, event, other=None):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    with transaction.atomic():
        if not User.objects.filter(id=user_id).exists():
            return None

        subscriber = (
            EventSubscriber.objects.select_for_update()
            .filter(user_id=user_id, event=event, other=other)
            .first()
        )

        if not subscriber:
            EventSubscriber.objects.create(
                user_id=user_id,
                event=event,
                other=other,
                response=None,
                last_check=timezone.now(),
            )
            return None

        if subscriber.response is None:
            subscriber.last_check = timezone.now()
            subscriber.save(update_fields=["last_check"])
            return None
        else:
            response_data = json.loads(subscriber.response)
            subscriber.response = None
            subscriber.last_check = timezone.now()
            subscriber.save(update_fields=["response", "last_check"])
            return response_data


def set_event_response(event, other, response):
    response_value = (
        json.dumps(response, ensure_ascii=False, cls=DjangoJSONEncoder)
        if response is not None
        else None
    )

    return EventSubscriber.objects.filter(event=event, other=other).update(
        response=response_value, last_check=timezone.now()
    )
