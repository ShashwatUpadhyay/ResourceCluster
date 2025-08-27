from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # If remember me is not checked, expire session when browser closes
            if not remember:
                request.session.set_expiry(0)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'base/login.html', {'error_message': error_message})
    
    return render(request, 'base/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validate form data
        if password1 != password2:
            error_message = 'Passwords do not match'
            return render(request, 'base/register.html', {'error_message': error_message})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            error_message = 'Username already exists'
            return render(request, 'base/register.html', {'error_message': error_message})
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            error_message = 'Email already exists'
            return render(request, 'base/register.html', {'error_message': error_message})
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        # Log user in
        login(request, user)
        
        # Redirect to home page
        return redirect('home')
    
    return render(request, 'base/register.html')

def upload_view(request):
    # Get data for dropdowns
    course = Cource.objects.all()
    subject = Subject.objects.all()
    session = Session.objects.all()
    
    context = {
        'course': course,
        'subject': subject,
        'session': session,
        'category': RESOURCE_CATEGORY,
        'type': RESOURCE_TYPE,
    }
    
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        resource_type = request.POST.get('resource_type')
        course_id = request.POST.get('course')
        subject_id = request.POST.get('subject')
        session_id = request.POST.get('session')
        category = request.POST.get('category')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        
        # Validate file size (10MB limit)
        if file.size > 10 * 1024 * 1024:  # 10MB in bytes
            context['error_message'] = 'File size exceeds the maximum limit of 10MB.'
            return render(request, 'base/upload.html', context)
        
        # Validate file type
        allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                        'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/zip']
        
        if file.content_type not in allowed_types:
            context['error_message'] = 'Invalid file type. Please upload a supported format.'
            return render(request, 'base/upload.html', context)
        
        try:
            # Get related objects
            course_obj = Cource.objects.get(id=course_id)
            subject_obj = Subject.objects.get(id=subject_id)
            session_obj = Session.objects.get(id=session_id)
            
            # Create resource
            from resource.models import Resource
            resource = Resource.objects.create(
                name=title,
                type=resource_type,
                course=course_obj,
                subject=subject_obj,
                session=session_obj,
                category=category,
                description=description,
                file=file,
                created_by=request.user
            )
            
            context['success_message'] = 'Resource uploaded successfully!'
            # Clear form data after successful upload
            return render(request, 'base/upload.html', context)
            
        except Exception as e:
            context['error_message'] = f'An error occurred: {str(e)}'
            return render(request, 'base/upload.html', context)
    
    return render(request, 'base/upload.html', context)
