from django import forms
from django.utils.text import slugify
from markdownx.fields import MarkdownxFormField
from .models import BlogPost, Comment, Category, Tag


class BlogPostForm(forms.ModelForm):
    content = MarkdownxFormField(
        help_text="Write your blog content in Markdown format. You can use headers, lists, code blocks, links, and more!"
    )
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'category', 'tags', 'content', 'excerpt', 
            'featured_image', 'status', 'is_featured', 
            'meta_title', 'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of your post (optional)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO title (optional)'
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO description (optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select a category"
        self.fields['tags'].queryset = Tag.objects.all()

    def clean_title(self):
        title = self.cleaned_data['title']
        slug = slugify(title)
        
        # Check if slug already exists (excluding current instance if editing)
        existing_posts = BlogPost.objects.filter(slug=slug)
        if self.instance.pk:
            existing_posts = existing_posts.exclude(pk=self.instance.pk)
        
        if existing_posts.exists():
            raise forms.ValidationError('A post with this title already exists.')
        
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content.strip()) < 10:
            raise forms.ValidationError('Comment must be at least 10 characters long.')
        return content


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Category description (optional)'
            })
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tag name'
            })
        }


class BlogSearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search blog posts...',
            'type': 'search'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        empty_label="All Tags",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )