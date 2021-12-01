from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    post_title = models.CharField(max_length=100, blank=False)
    post_body = models.TextField(blank=False)
    date_added = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, default='')
    img = models.ImageField(upload_to='')

    def __str__(self) -> str:
        return self.post_title

