from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from resource.models import Cource,Subject,Session,Tag
from .choices import RESOURCE_CATEGORY,RESOURCE_TYPE,SEMESTER_CHOICE
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
        'semester':SEMESTER_CHOICE,
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
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    
    course = Cource.objects.all()
    subject = Subject.objects.all()
    session = Session.objects.all()
    tags = Tag.objects.filter().distinct()
    
    context = {
        'course': course,
        'subject': subject,
        'session': session,
        'tags': tags,
        'category': RESOURCE_CATEGORY,
        'type': RESOURCE_TYPE,
        'semester':SEMESTER_CHOICE,
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
        tags = request.POST.getlist('tags[]')
        semester = request.POST.get('semester')
        url = request.POST.get('url')
        print(url,file)
        if not file and not url:
            context['error_message'] = 'Please upload a file or enter a URL.'
            return render(request, 'base/upload.html', context)
        
        # Validate file size (10MB limit)
        if file and file.size > 10 * 1024 * 1024:  # 10MB in bytes
            context['error_message'] = 'File size exceeds the maximum limit of 10MB.'
            return render(request, 'base/upload.html', context)
        
        # Validate file type
        allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                        'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/zip']
        
        if file and file.content_type not in allowed_types:
            context['error_message'] = 'Invalid file type. Please upload a supported format.'
            return render(request, 'base/upload.html', context)
        
        try:
            # Get related objects
            course_obj = Cource.objects.get(id=course_id)
            subject_obj = Subject.objects.get(id=subject_id)
            session_obj = Session.objects.get(id=session_id)
            
            # Get tags
            tag_ids = request.POST.getlist('tags[]')
            
            # Create resource
            from resource.models import Resource
            resource = Resource.objects.create(
                name=title,
                type=resource_type,
                course=course_obj,
                subject=subject_obj,
                session=session_obj,
                category=category,
                semester=semester,
                description=description,
                created_by=request.user
            )
            if file:
                resource.file = file
            else:
                resource.url = url
            resource.save()
            for tag in tags:
                tag_obj , _ = Tag.objects.get_or_create(name=tag)
                resource.tags.add(tag_obj)
            # Process tags (both existing and new)
            for tag_id in tag_ids:
                # Check if it's a numeric ID (existing tag) or a new tag name
                if tag_id.isdigit():
                    # Existing tag
                    try:
                        tag = Tag.objects.get(id=int(tag_id))
                        resource.tags.add(tag)
                    except Tag.DoesNotExist:
                        pass
                else:
                    # New tag - create it
                    new_tag, created = Tag.objects.get_or_create(name=tag_id)
                    resource.tags.add(new_tag)
            
            context['success_message'] = 'Resource uploaded successfully!'
            # Clear form data after successful upload
            # return render(request, 'base/upload.html', context)
            messages.success(request, 'Resource uploaded successfully!')
            return redirect('upload_resource')
            
        except Exception as e:
            context['error_message'] = f'An error occurred: {str(e)}'
            return render(request, 'base/upload.html', context)
    
    return render(request, 'base/upload.html', context)
