from django.db import models

# Create your models here.
class User(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('merchant', 'Merchant'),
    )

    name = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.role})"