from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
import re


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    content = MarkdownxField(help_text="Write your blog content in Markdown format")
    excerpt = models.TextField(
        max_length=300, blank=True, help_text="Brief description of the post")
    featured_image = models.ImageField(
        upload_to='blog/images/', blank=True, null=True)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)

    meta_title = models.CharField(
        max_length=60, blank=True, help_text="SEO title")
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="SEO description")

    views_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()

        # Generate excerpt if not provided
        if not self.excerpt and self.content:
            self.excerpt = self.get_excerpt_from_content()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('blog:post_edit', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('blog:post_delete', kwargs={'slug': self.slug})

    @property
    def reading_time(self):
        """Calculate estimated reading time in minutes"""
        # Remove markdown syntax for accurate word count
        plain_text = self.get_plain_text_content()
        word_count = len(plain_text.split())
        return max(1, word_count // 200)  # Assuming 200 words per minute

    def get_markdown_content(self):
        """Convert markdown content to HTML"""
        return markdownify(self.content)

    def get_plain_text_content(self):
        """Extract plain text from markdown content"""
        # Remove markdown syntax
        plain_text = re.sub(r'[#*`_~\[\]()]+', '', self.content)
        plain_text = re.sub(r'!\[.*?\]\(.*?\)', '', plain_text)  # Remove images
        plain_text = re.sub(r'\[.*?\]\(.*?\)', '', plain_text)   # Remove links
        plain_text = re.sub(r'```.*?```', '', plain_text, flags=re.DOTALL)  # Remove code blocks
        plain_text = re.sub(r'`.*?`', '', plain_text)  # Remove inline code
        plain_text = re.sub(r'\n+', ' ', plain_text)  # Replace newlines with spaces
        return plain_text.strip()

    def get_excerpt_from_content(self):
        """Generate excerpt from markdown content"""
        plain_text = self.get_plain_text_content()
        if len(plain_text) > 297:
            return plain_text[:297] + "..."
        return plain_text


class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    @property
    def is_reply(self):
        return self.parent is not None
