from django.db import models
from base.models import BaseModel
# Create your models here.
class Department(BaseModel):
    name = models.CharField(max_length=255)


class CollegeStaff(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='staff/')
    position = models.CharField(max_length=255)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)