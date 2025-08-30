from django.db import models
from base.models import BaseModel
from base.choices import RESOURCE_CATEGORY,RESOURCE_TYPE,SEMESTER_CHOICE

# Create your models here.

class Cource(BaseModel):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'cource'

class Subject(BaseModel):
    name = models.CharField(max_length=255)
    course = models.ForeignKey('Cource', on_delete=models.CASCADE, null=True,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'subject'
        ordering = ['name']

class Session(BaseModel):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'session'
        ordering = ['name']
        

class Tag(BaseModel):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'tag'


class Resource(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField('Tag')
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=RESOURCE_CATEGORY, default='image')
    type = models.CharField(max_length=255, choices=RESOURCE_TYPE, default='note')
    course = models.ForeignKey('Cource', on_delete=models.CASCADE)
    semester = models.CharField(max_length=255, choices=SEMESTER_CHOICE, default='1')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'resource'
        ordering = ['-created_at']
