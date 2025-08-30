from django.db import models
import uuid
# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
    
    
    
from django.utils import timezone
from django.contrib.auth.models import User

class Notification(BaseModel):
    NOTIFICATION_TYPES = [
        ('resource_upload', 'Resource Upload'),
        ('user_registration', 'User Registration'),
        ('system', 'System Notification'),
    ]
    
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    is_read = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return self.message[:50]