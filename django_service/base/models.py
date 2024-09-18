from django.db import models

# Create your models here.
class User(models.Model):
    
    username = models.CharField(max_length=100, null=False, blank=False)
    
class Book(models.Model):
    
    book_name = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=100, null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)