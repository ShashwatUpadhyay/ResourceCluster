from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Tag, BlogPost
from django.utils.text import slugify
import random


class Command(BaseCommand):
    help = 'Populate blog with sample data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Technology', 'description': 'Latest tech trends and tutorials'},
            {'name': 'Programming', 'description': 'Coding tips and best practices'},
            {'name': 'Web Development', 'description': 'Frontend and backend development'},
            {'name': 'Data Science', 'description': 'Data analysis and machine learning'},
            {'name': 'Mobile Development', 'description': 'iOS and Android development'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create tags
        tags_data = [
            'Python', 'JavaScript', 'Django', 'React', 'Vue.js', 'Node.js',
            'Machine Learning', 'AI', 'Tutorial', 'Guide', 'Tips', 'Best Practices',
            'Frontend', 'Backend', 'Database', 'API', 'Security', 'Performance'
        ]

        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag.name}')

        # Get or create a user for blog posts
        user, created = User.objects.get_or_create(
            username='blogger',
            defaults={
                'email': 'blogger@example.com',
                'first_name': 'Blog',
                'last_name': 'Writer'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write('Created blogger user')

        # Sample blog posts
        posts_data = [
            {
                'title': 'Getting Started with Django Web Development',
                'content': '''# Getting Started with Django Web Development

Django is a **high-level Python web framework** that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

In this comprehensive guide, we'll walk through the basics of Django development, from setting up your environment to deploying your first application.

## Why Choose Django?

Django follows the *"batteries-included"* philosophy, providing many built-in features that make web development faster and more secure. Some key advantages include:

- **Rapid Development**: Django's design helps developers take applications from concept to completion as quickly as possible.
- **Security**: Django helps developers avoid many common security mistakes by providing a framework that has been engineered to "do the right things" to protect the website automatically.
- **Scalability**: Some of the busiest sites on the web leverage Django's ability to quickly and flexibly scale.

## Setting Up Your Environment

Before we start building with Django, we need to set up our development environment. Here's what you'll need:

1. Python 3.8 or higher
2. pip (Python package installer)
3. Virtual environment (recommended)

### Installation Steps

```bash
# Create a virtual environment
python -m venv myenv

# Activate the virtual environment
# On Windows:
myenv\\Scripts\\activate
# On macOS/Linux:
source myenv/bin/activate

# Install Django
pip install django
```

> **Pro Tip**: Always use virtual environments to keep your project dependencies isolated!

## Creating Your First Project

Let's create a new Django project:

```python
# Create a new Django project
django-admin startproject myproject

# Navigate to the project directory
cd myproject

# Run the development server
python manage.py runserver
```

Your Django application is now running at `http://127.0.0.1:8000/`!

## Next Steps

- Learn about Django models and databases
- Explore the Django admin interface
- Build your first views and templates
- Deploy your application to production

Happy coding!''',
                'excerpt': 'Learn the fundamentals of Django web development in this comprehensive beginner-friendly guide.',
                'category': 'Web Development',
                'tags': ['Python', 'Django', 'Tutorial', 'Backend'],
                'is_featured': True
            },
            {
                'title': 'Modern JavaScript ES6+ Features You Should Know',
                'content': '''# Modern JavaScript ES6+ Features You Should Know

JavaScript has evolved significantly over the years, and **ES6 (ECMAScript 2015)** introduced many powerful features that have transformed how we write JavaScript code. In this post, we'll explore the most important ES6+ features that every developer should master.

## Arrow Functions

Arrow functions provide a more concise way to write function expressions:

```javascript
// Traditional function
function add(a, b) {
    return a + b;
}

// Arrow function
const add = (a, b) => a + b;

// Even shorter for single expressions
const square = x => x * x;
```

### Benefits of Arrow Functions:
- Shorter syntax
- Lexical `this` binding
- Implicit return for single expressions

## Template Literals

Template literals make string interpolation much cleaner and support multi-line strings:

```javascript
const name = 'John';
const age = 30;

// Old way
const message = 'Hello, my name is ' + name + ' and I am ' + age + ' years old.';

// Template literals
const message = `Hello, my name is ${name} and I am ${age} years old.`;

// Multi-line strings
const html = `
  <div>
    <h1>${name}</h1>
    <p>Age: ${age}</p>
  </div>
`;
```

## Destructuring Assignment

Destructuring allows you to extract values from arrays or objects:

```javascript
// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
console.log(first); // 1
console.log(rest);  // [3, 4, 5]

// Object destructuring
const {name, age, city = 'Unknown'} = {
  name: 'John', 
  age: 30, 
  country: 'USA'
};
```

## Spread Operator

The spread operator (`...`) is incredibly versatile:

```javascript
// Array spreading
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5]; // [1, 2, 3, 4, 5]

// Object spreading
const obj1 = {a: 1, b: 2};
const obj2 = {...obj1, c: 3}; // {a: 1, b: 2, c: 3}

// Function arguments
const numbers = [1, 2, 3];
Math.max(...numbers); // equivalent to Math.max(1, 2, 3)
```

## Default Parameters

Set default values for function parameters:

```javascript
function greet(name = 'World', greeting = 'Hello') {
  return `${greeting}, ${name}!`;
}

greet(); // "Hello, World!"
greet('John'); // "Hello, John!"
greet('Jane', 'Hi'); // "Hi, Jane!"
```

## Modules

ES6 modules provide a standardized way to organize code:

```javascript
// math.js
export const PI = 3.14159;
export function add(a, b) {
  return a + b;
}
export default function multiply(a, b) {
  return a * b;
}

// main.js
import multiply, { PI, add } from './math.js';
```

## Classes

ES6 classes provide a cleaner syntax for object-oriented programming:

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }
  
  speak() {
    console.log(`${this.name} makes a sound`);
  }
}

class Dog extends Animal {
  speak() {
    console.log(`${this.name} barks`);
  }
}

const dog = new Dog('Rex');
dog.speak(); // "Rex barks"
```

## Promises and Async/Await

Handle asynchronous operations more elegantly:

```javascript
// Promises
fetch('/api/data')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));

// Async/Await
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}
```

## Conclusion

These ES6+ features make JavaScript code more **readable**, **maintainable**, and **powerful**. Start incorporating them into your projects today!

> **Remember**: Modern JavaScript is constantly evolving. Stay updated with the latest features and best practices!''',
                'excerpt': 'Discover the most important ES6+ JavaScript features that will improve your code quality and productivity.',
                'category': 'Programming',
                'tags': ['JavaScript', 'Frontend', 'Tutorial'],
                'is_featured': True
            },
            {
                'title': 'Building RESTful APIs with Django REST Framework',
                'content': '''# Building RESTful APIs with Django REST Framework

**Django REST Framework (DRF)** is a powerful toolkit for building Web APIs in Django. It provides a comprehensive set of tools and libraries that make it easy to build robust, scalable APIs with minimal code.

## What is REST?

**REST (Representational State Transfer)** is an architectural style for designing networked applications. RESTful APIs use standard HTTP methods to perform operations on resources:

| HTTP Method | Purpose | Example |
|-------------|---------|---------|
| GET | Retrieve data | `GET /api/posts/` |
| POST | Create new resource | `POST /api/posts/` |
| PUT | Update entire resource | `PUT /api/posts/1/` |
| PATCH | Partial update | `PATCH /api/posts/1/` |
| DELETE | Remove resource | `DELETE /api/posts/1/` |

## Setting Up Django REST Framework

First, install DRF in your Django project:

```bash
pip install djangorestframework
pip install djangorestframework-simplejwt  # For JWT authentication
```

Add it to your `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Add this
    'rest_framework.authtoken',  # For token authentication
    # ... your apps
]

# DRF Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

## Creating Your First API

Let's create a simple API for a blog application:

### 1. Define the Model

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
```

### 2. Create Serializers

```python
# serializers.py
from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'author_name', 
                 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Automatically set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
```

### 3. Create ViewSets

```python
# views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = BlogPost.objects.all()
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__username=author)
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """Get current user's posts"""
        posts = BlogPost.objects.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
```

### 4. Configure URLs

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.BlogPostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
```

## Authentication & Permissions

### Token Authentication

```python
# Create tokens for users
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create token for a user
user = User.objects.get(username='john')
token, created = Token.objects.get_or_create(user=user)
print(token.key)
```

### Custom Permissions

```python
# permissions.py
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the author
        return obj.author == request.user
```

## Testing Your API

```python
# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import BlogPost

class BlogPostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_post(self):
        data = {
            'title': 'Test Post',
            'content': 'This is a test post content.'
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 1)
```

## API Endpoints

Your API will automatically provide these endpoints:

- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create a new post
- `GET /api/posts/{id}/` - Retrieve a specific post
- `PUT /api/posts/{id}/` - Update a post
- `PATCH /api/posts/{id}/` - Partially update a post
- `DELETE /api/posts/{id}/` - Delete a post
- `GET /api/posts/my_posts/` - Get current user's posts

## Best Practices

1. **Use proper HTTP status codes**
2. **Implement pagination for large datasets**
3. **Add proper authentication and permissions**
4. **Use serializers for data validation**
5. **Write comprehensive tests**
6. **Document your API with tools like Swagger**

## Conclusion

Django REST Framework makes it incredibly easy to build powerful APIs with just a few lines of code. The framework handles serialization, authentication, permissions, and much more out of the box!

> **Next Steps**: Explore advanced features like custom serializers, filtering, searching, and API documentation with `drf-spectacular`.''',
                'excerpt': 'Learn how to build powerful RESTful APIs using Django REST Framework with practical examples.',
                'category': 'Web Development',
                'tags': ['Django', 'API', 'Backend', 'Tutorial'],
                'is_featured': False
            }
        ]

        for post_data in posts_data:
            # Check if post already exists
            if not BlogPost.objects.filter(title=post_data['title']).exists():
                category = Category.objects.get(name=post_data['category'])
                
                post = BlogPost.objects.create(
                    title=post_data['title'],
                    content=post_data['content'],
                    excerpt=post_data['excerpt'],
                    author=user,
                    category=category,
                    status='published',
                    is_featured=post_data['is_featured'],
                    views_count=random.randint(50, 500)
                )
                
                # Add tags
                post_tags = [Tag.objects.get(name=tag_name) for tag_name in post_data['tags']]
                post.tags.set(post_tags)
                
                self.stdout.write(f'Created blog post: {post.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated blog with sample data!'))