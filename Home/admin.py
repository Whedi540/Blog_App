from django.contrib import admin
from .models import BlogPost
# Register your models here.


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')  # Fields to display in the list view
    search_fields = ('title', 'content')  # Make these fields searchable
    list_filter = ('created_at',)  # Add filtering by created date

admin.site.register(BlogPost, BlogPostAdmin)  # Register the model with the custom admin configuration