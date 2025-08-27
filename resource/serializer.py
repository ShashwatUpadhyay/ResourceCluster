from rest_framework import serializers
from .models import Resource,Tag

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class ResourceSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.name')
    course = serializers.CharField(source='course.name')
    session = serializers.CharField(source='session.name')
    created_by = serializers.CharField(source='created_by.get_full_name')
    tags = TagsSerializer(many=True)
    class Meta:
        model = Resource
        exclude = ['id','updated_at']
