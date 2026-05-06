from django.db import models
from users.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    points_required = models.IntegerField()
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    merchant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'merchant'}
    )
    
    def __str__(self):
        return self.name