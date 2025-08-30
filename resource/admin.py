from django.contrib import admin
from .models import Resource,Tag,Cource,Session,Subject
from base.models import Notification
# Register your models here.
admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(Cource)
admin.site.register(Session)
admin.site.register(Subject)
admin.site.register(Notification)
