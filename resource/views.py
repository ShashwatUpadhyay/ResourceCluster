from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ResourceSerializer
from .models import Resource

# Create your views here.

class ListResourcesAPIView(APIView):
    def get(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response({
            'status': 200,
            'message': 'Resources fetched successfully',
            'data': serializer.data
        })