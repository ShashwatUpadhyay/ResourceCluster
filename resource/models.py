from django.db import models
from base.models import BaseModel
from base.choices import RESOURCE_CATEGORY,RESOURCE_TYPE

# Create your models here.

class Cource(BaseModel):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'cource'

class Subject(BaseModel):
    name = models.CharField(max_length=255)
    course = models.ForeignKey('Cource', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'subject'

class Session(BaseModel):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'session'

class Tag(BaseModel):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'tag'


class Resource(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')
    tags = models.ManyToManyField('Tag')
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=RESOURCE_CATEGORY, default='image')
    type = models.CharField(max_length=255, choices=RESOURCE_TYPE, default='note')
    course = models.ForeignKey('Cource', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'resource'
        ordering = ['-created_at']
