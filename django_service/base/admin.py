from django.contrib import admin

from base.models.book.book import Book
from base.models.user.user import User

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    
    """Admin panel customization for Book model."""
    
    list_display = (
        'book_name', 
        'author', 
        'isbn', 
        'publisher', 
        'publication_date', 
        'uploaded_at', 
        'uploaded_by',
    )
    list_filter = (
        'publication_date', 
        'uploaded_at', 
        'publisher',
    )
    search_fields = (
        'book_name', 
        'author', 
        'isbn',
    )
    ordering = ('-uploaded_at',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    """Admin panel customization for User model."""
    
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_active', 
        'date_joined',
    )
    list_filter = (
        'is_active', 
        'date_joined',
    )
    search_fields = (
        'username', 
        'email', 
        'first_name', 
        'last_name',
    )
    ordering = ('username',)
