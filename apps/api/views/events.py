from rest_framework.views import APIView
from rest_framework.response import Response
from apps.api.services.event import check_event

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.api.services.event import check_event

class EventCheckView(APIView):
    def post(self, request):
        if not request.user or not request.user.is_authenticated:
            user_id = request.data.get('user_id')
            event = request.data.get('event')
            other = request.data.get('other')
            result = check_event(user_id, event, other)
            return Response({'response': result, 'stop': True}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.data.get('user_id')
        event = request.data.get('event')
        other = request.data.get('other')
        result = check_event(user_id, event, other)
        return Response({'response': result, 'delay': 60000})
