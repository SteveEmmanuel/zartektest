import datetime as datetime
from django.contrib.auth.models import User
from django.db import models


class PostImage(models.Model):
    """Model representing an Image in a Post."""
    image = models.ImageField(upload_to='images/')

    # todo delete image when row is deleted
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=False, related_name='images')


class Post(models.Model):
    """Model representing a Post."""

    description = models.TextField(max_length=1000, null=False, help_text='Enter a brief description of the post')

    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    datetime = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False)


class PostTag(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, null=False, related_name='post_tags')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=False, related_name='post_tags')

    weight = models.IntegerField(null=False)
