from django.db import models

from django_service.base.models.user.user import User

class Book(models.Model):
    
    book_name = models.CharField (
        max_length=100, 
        null=False, 
        blank=False,
    )
    author = models.CharField (
        max_length=100, 
        null=False, 
        blank=False,
    )
    description = models.TextField (
        null=True, 
        blank=True, 
        help_text="Краткое описание книги",
    )
    isbn = models.CharField (
        max_length=13, 
        unique=True, 
        null=True, 
        blank=True, 
        help_text="13-значный ISBN",
    )
    publisher = models.CharField (
        max_length=100, 
        null=True, 
        blank=True,
    )
    publication_date = models.DateField (
        null=True, 
        blank=True,
    )
    uploaded_at = models.DateTimeField (
        auto_now_add=True,
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
    )

    def __str__(self):
        return f"{self.book_name} by {self.author}"

    class Meta:
        ordering = ['-uploaded_at']
