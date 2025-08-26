from django.urls import path
from resource.views import ListResourcesAPIView

urlpatterns = [
    path('resources/', ListResourcesAPIView.as_view(), name='list-resources'),
]
