from django.shortcuts import render
from rest_framework.views import APIView
from .models import YTVideo
from .serializer import YTVideoSerializer
from rest_framework.response import Response

class YTVideoView(APIView):
    def get(self, request):
        output = [
            {
                'title': out.title,
                'author': out.author
            } for out in YTVideo.objects.all()
        ]
        return Response(output)
    
    def post(self, request):
        serializer = YTVideoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
