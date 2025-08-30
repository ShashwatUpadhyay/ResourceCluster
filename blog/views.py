from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.utils import timezone
from .models import BlogPost, Category, Tag, Comment
from .forms import BlogPostForm, CommentForm


def blog_home(request):
    """Blog home page with featured posts and recent posts"""
    featured_posts = BlogPost.objects.filter(status='published', is_featured=True)[:3]
    recent_posts = BlogPost.objects.filter(status='published').exclude(is_featured=True)[:6]
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:10]
    popular_tags = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)[:15]
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'popular_tags': popular_tags,
    }
    return render(request, 'blog/home.html', context)


def post_list(request):
    """List all published posts with pagination and filtering"""
    posts = BlogPost.objects.filter(status='published')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Tag filter
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Pagination
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Individual blog post detail page"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment view count
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    # Get comments
    comments = post.comments.filter(is_approved=True, parent=None).prefetch_related('replies')
    
    # Related posts
    related_posts = BlogPost.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    # Comment form
    comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='login')
def post_create(request):
    """Create a new blog post"""
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Blog post created successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'title': 'Create New Post',
        'button_text': 'Create Post'
    })


@login_required(login_url='login')
def post_edit(request, slug):
    """Edit an existing blog post"""
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Check if user is the author or has permission
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('blog:post_detail', slug=post.slug)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'post': post,
        'title': 'Edit Post',
        'button_text': 'Update Post'
    })


@login_required(login_url='login')
def post_delete(request, slug):
    """Delete a blog post"""
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Check if user is the author or has permission
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('blog:post_detail', slug=post.slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('blog:post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required(login_url='login')
def my_posts(request):
    """User's own blog posts"""
    posts = BlogPost.objects.filter(author=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        posts = posts.filter(status=status_filter)
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'blog/my_posts.html', context)


def category_posts(request, slug):
    """Posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(category=category, status='published')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """Posts by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = BlogPost.objects.filter(tags=tag, status='published')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_posts.html', context)


@login_required(login_url='login')
@require_POST
def add_comment(request, slug):
    """Add a comment to a blog post"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        
        # Handle reply to another comment
        parent_id = request.POST.get('parent_id')
        if parent_id:
            comment.parent = get_object_or_404(Comment, id=parent_id)
        
        comment.save()
        messages.success(request, 'Your comment has been added!')
    else:
        messages.error(request, 'There was an error with your comment.')
    
    return redirect('blog:post_detail', slug=slug)


def search_posts(request):
    """Search blog posts"""
    query = request.GET.get('q', '')
    posts = BlogPost.objects.none()
    
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            status='published'
        ).distinct()
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'total_results': posts.count(),
    }
    return render(request, 'blog/search_results.html', context)


def markdown_guide(request):
    """Markdown writing guide for users"""
    return render(request, 'blog/markdown_guide.html')
