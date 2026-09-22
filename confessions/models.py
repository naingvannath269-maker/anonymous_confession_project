from accounts.models import CustomUser
from django.db import models


class Confession(models.Model):
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  content = models.TextField(max_length=500)
  created_at = models.DateTimeField(auto_now_add=True)
  upvotes = models.PositiveIntegerField(default=0)
  is_approved = models.BooleanField(
      default=True
  )  # Set to False if you want manual moderation

  def __str__(self):
    return f'Confession by @{self.author.username} at {self.created_at}'