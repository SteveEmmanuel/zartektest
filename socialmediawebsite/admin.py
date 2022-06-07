from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Post, PostImage

admin.site.unregister(Group)

admin.site.register(Post)
admin.site.register(PostImage)
