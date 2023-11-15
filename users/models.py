from django.db import models
from django.contrib.auth.models import AbstractUser
from litrevu import settings


class User(AbstractUser):
    """Model used to manage User system, herited from django standard User model"""

    def __str__(self):
        return f'{self.username}'


class UserFollows(models.Model):
    """Model used to manage following system"""
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,  # which model is related to
        on_delete=models.CASCADE,  # behavior to adopt when the parent model is deleted
        related_name="following",  # name to use for reverse relation with the target model
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'followed_user'], name='unique_follow')
        ]


class UserBlocked(models.Model):
    """Model used to manage blocking user system"""
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user"
    )

    blocked_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_blocked"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'blocked_user'], name='unique_block')
        ]
