from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Discussion'),
        ('reviews', 'Reviews'),
        ('recommendations', 'Recommendations'),
    ]

    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='posts',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    pinned = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Reply(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='replies',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='replies',
    )
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Reply by {self.author} on {self.post}'


class Rules(models.Model):
    content = models.TextField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rules'
        verbose_name_plural = 'Rules'

    def __str__(self):
        return 'Community Rules'
