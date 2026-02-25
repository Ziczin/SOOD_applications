import json
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from apps.users.models import EventSubscriber


def set_event_response_for_all(event: str, response):
    now = timezone.now()
    cutoff = now - timedelta(minutes=10)
    EventSubscriber.objects.filter(last_check__lt=cutoff).delete()
    payload_text = (
        None if response is None else json.dumps(response, ensure_ascii=False)
    )
    subscribers = EventSubscriber.objects.select_for_update().filter(event=event)
    with transaction.atomic():
        for sub in subscribers:
            if not sub.response:
                sub.response = payload_text
                sub.last_check = now
                sub.save(update_fields=["response", "last_check"])
            else:
                EventSubscriber.objects.create(
                    user=sub.user,
                    event=sub.event,
                    response=payload_text,
                    last_check=now,
                )
