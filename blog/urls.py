from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog home and listing
    path('', views.blog_home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('search/', views.search_posts, name='search'),
    
    # Post CRUD operations
    path('create/', views.post_create, name='post_create'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('<slug:slug>/delete/', views.post_delete, name='post_delete'),
    
    # Comments
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    
    # Categories and Tags
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    
    # Markdown Guide
]