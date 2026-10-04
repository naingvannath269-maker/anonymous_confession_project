from accounts.models import CustomUser
from django.db import models


class Confession(models.Model):
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  content = models.TextField(max_length=500)
  created_at = models.DateTimeField(auto_now_add=True)
  is_approved = models.BooleanField(
      default=True
  )  # Set to False if you want manual moderation

  def __str__(self):
    return f'Confession by @{self.author.username} at {self.created_at}'


class Reaction(models.Model):
  user = models.ForeignKey(
      CustomUser,
      on_delete=models.CASCADE,
      related_name='confession_reactions',
  )
  confession = models.ForeignKey(
      Confession,
      on_delete=models.CASCADE,
      related_name='reactions',
  )
  is_like = models.BooleanField(default=True)

  class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=('user', 'confession'),
            name='unique_user_confession_reaction',
        ),
    ]