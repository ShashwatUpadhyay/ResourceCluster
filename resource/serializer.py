from rest_framework import serializers
from .models import Resource,Subject,Session,Tag

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class ResourceSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.name')
    course = serializers.CharField(source='course.name')
    session = serializers.CharField(source='session.name')
    created_by = serializers.CharField(source='created_by.username')
    tags = TagsSerializer(many=True)
    class Meta:
        model = Resource
        exclude = ['id','updated_at']
