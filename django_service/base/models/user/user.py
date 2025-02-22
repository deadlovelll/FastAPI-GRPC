from django.db import models

class User(models.Model):
    
    username = models.CharField (
        max_length=100, 
        null=False, 
        blank=False, 
        unique=True,
    )
    email = models.EmailField (
        max_length=254, 
        null=False, 
        blank=False, 
        unique=True,
    )
    first_name = models.CharField (
        max_length=50, 
        null=True, 
        blank=True,
    )
    last_name = models.CharField (
        max_length=50, 
        null=True, 
        blank=True,
    )
    is_active = models.BooleanField (
        default=True,
    )
    date_joined = models.DateTimeField (
        auto_now_add=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']