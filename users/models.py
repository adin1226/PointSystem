from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('member', '會員'),
        ('merchant', '店家'),
        ('admin', '管理員'),
    )
    
    # name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} ({self.role})"