import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import formset_factory, BaseFormSet, ValidationError
from django.shortcuts import render
from django.views import View
from .models import Post, PostImage, PostTag, Tag
from .forms import PostForm, TagForm


class CustomFormset(BaseFormSet):

    def clean(self):
        weight_sum = 0
        for tag in self.cleaned_data:
            if tag['name'] != '':
                weight_sum += tag['weight']
        if weight_sum != 100:
            raise ValidationError("The sum total of weight should be 100")


class PostListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'socialmediawebsite.can_add_post'

    def get(self, request, *args, **kwargs):
        logged_in_user = request.user

        posts = Post.objects.all()
        form = PostForm()

        TagFormSet = formset_factory(TagForm, formset=CustomFormset)
        tag_formset = TagFormSet()

        context = {
            'post_list': posts,
            'form': form,
            'formset': tag_formset,
        }

        return render(request, 'feed.html', context)

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.all()
        form = PostForm(request.POST, request.FILES)

        TagFormSet = formset_factory(TagForm, formset=CustomFormset)
        tag_formset = TagFormSet(data=request.POST)

        files = request.FILES.getlist('image')

        if form.is_valid() and tag_formset.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.datetime = datetime.datetime.now()
            new_post.save()

            for f in files:
                image = PostImage(image=f)
                image.post = new_post
                image.save()

            new_post.save()

            for tag_and_weight in tag_formset.cleaned_data:
                if not Tag.objects.filter(name=tag_and_weight['name']).exists():
                    tag = Tag(name=tag_and_weight['name'])
                    tag.save()
                else:
                    tag = Tag.objects.filter(name=tag_and_weight['name']).first()
                weight = tag_and_weight['weight']

                post_tag = PostTag(tag=tag, weight=weight, post=new_post)
                post_tag.save()

        formset_error_message = ""
        if not tag_formset.is_valid():
            formset_error_message = "Tag name and weight cannot be blank and sum of weights should be 100"

        context = {
            'post_list': posts,
            'form': form,
            'formset': tag_formset,
            'formset_error_message': formset_error_message
        }
        return render(request, 'feed.html', context)
