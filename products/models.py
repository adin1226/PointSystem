from django.db import models
from users.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    points_required = models.IntegerField()
    stock = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name