from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

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


class Comment(models.Model):
    sn = models.AutoField(primary_key=True)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)

    def __str__(self) -> str:
        return f'{self.comment[:20]}... By {self.author}'

