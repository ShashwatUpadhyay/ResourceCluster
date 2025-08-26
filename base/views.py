from django.shortcuts import render
from resource.models import Cource,Subject,Session
from .choices import RESOURCE_CATEGORY,RESOURCE_TYPE
# Create your views here.
def home(request):
    course = Cource.objects.all()
    subject = Subject.objects.all()
    session = Session.objects.all()
    data = {
        'course':course,
        'subject':subject,
        'session':session,
        'category':RESOURCE_CATEGORY,
        'type':RESOURCE_TYPE,
    }
    return render(request, 'base/index.html',data)
