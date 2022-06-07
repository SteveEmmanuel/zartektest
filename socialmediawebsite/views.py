import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import View
from .models import Post, PostImage
from .forms import PostForm

class PostListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'socialmediawebsite.can_add_post'

    def get(self, request, *args, **kwargs):
        logged_in_user = request.user

        posts = Post.objects.all()
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'feed.html', context)

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.all()
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.datetime = datetime.datetime.now()
            new_post.save()

            for f in files:
                image = PostImage(image=f)
                image.post = new_post
                image.save()

            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'feed.html', context)
