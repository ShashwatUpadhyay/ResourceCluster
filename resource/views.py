from django.db.models import F
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ResourceSerializer
from .models import Resource
from django.db.models import Q

# Create your views here.

class ListResourcesAPIView(APIView):
    def get(self, request):
        course = request.GET.get('course')
        subject = request.GET.get('subject')
        session = request.GET.get('session')
        semester = request.GET.get('semester')
        print(course, subject, session, semester)
        resources = Resource.objects.all()
        if course:
            resources = resources.filter(course__uid=course)
        if subject:
            resources = resources.filter(subject__uid=subject)
        if session:
            resources = resources.filter(session__uid=session)
        if semester:
            resources = resources.filter(semester=semester)
        serializer = ResourceSerializer(resources, many=True)
        return Response({
            'status': 200,
            'message': 'Resources fetched successfully',
            'data': serializer.data
        })