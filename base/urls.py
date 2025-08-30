from django.urls import path
from . import views
from blog.views import markdown_guide

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('upload/', views.upload_view, name='upload_resource'),
    path('markdown-guide/', markdown_guide, name='markdown_guide'),
    
]