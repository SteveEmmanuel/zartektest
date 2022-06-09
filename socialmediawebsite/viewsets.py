from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer, LikedUserSerializer
from rest_framework.response import Response

from itertools import chain


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    http_method_names = ['get', 'post']

    def list(self, request):
        logged_in_user = request.user
        liked_posts = Post.objects.filter(likes=logged_in_user).all()

        liked_posts_id_list = []
        for post in liked_posts:
            liked_posts_id_list.append(post.pk)
        liked_tags_and_weights = {}
        total_weight = 0
        for post in liked_posts.all():
            for post_tag in post.post_tags.all():
                total_weight += post_tag.weight
                if post_tag.tag.name in liked_tags_and_weights.keys():
                    liked_tags_and_weights[post_tag.tag.name] = post_tag.weight + liked_tags_and_weights[
                        post_tag.tag.name]
                else:
                    liked_tags_and_weights[post_tag.tag.name] = post_tag.weight

        liked_tags_and_weight_percentage = {}
        for liked_tags_and_weight in liked_tags_and_weights:
            liked_tags_and_weight_percentage[liked_tags_and_weight] = liked_tags_and_weights[
                                                                          liked_tags_and_weight] / total_weight

        liked_tags_list = [k for k, v in liked_tags_and_weights.items()]

        disliked_posts = Post.objects.filter(dislikes=logged_in_user).all()
        disliked_tags_and_weights = {}
        for post in disliked_posts.all():
            for post_tag in post.post_tags.all():
                if post_tag.tag.name in disliked_tags_and_weights.keys():
                    disliked_tags_and_weights[post_tag.tag.name] = post_tag.weight + disliked_tags_and_weights[
                        post_tag.tag.name]
                else:
                    disliked_tags_and_weights[post_tag.tag.name] = post_tag.weight

        disliked_tags_list = [k for k, v in disliked_tags_and_weights.items()]

        similar_posts = Post.objects.exclude(pk__in=liked_posts_id_list).filter(
            post_tags__tag__name__in=liked_tags_list).exclude(
            post_tags__tag__name__in=disliked_tags_list)

        similar_posts_with_score_dict = {}
        for post in similar_posts.all():
            score = 0
            for tag_and_weight in liked_tags_and_weight_percentage:
                for post_tag in post.post_tags.all():
                    if tag_and_weight == post_tag.tag.name:
                        score += liked_tags_and_weight_percentage[tag_and_weight] * post_tag.weight

            similar_posts_with_score_dict[post] = score

        similar_posts_sorted_list = [k for k, v in
                                     sorted(similar_posts_with_score_dict.items(), key=lambda item: item[1],
                                            reverse=True)]

        other_posts = Post.objects.exclude(pk__in=liked_posts_id_list).exclude(
            post_tags__tag__name__in=liked_tags_list).exclude(post_tags__tag__name__in=disliked_tags_list)

        sorted_posts = list(chain(similar_posts_sorted_list, other_posts, liked_posts, disliked_posts))

        serializer = PostSerializer(sorted_posts, many=True, context={
            'request': request
        })
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk, )
        serializer = PostSerializer(post, context={
            'request': request
        })
        return Response(serializer.data)

    @action(detail=True, url_path='likedusers')
    def liked_users(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        users = post.likes.all()
        serializer = LikedUserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='like')
    def like_post(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(post, context={
            'request': request})

        logged_in_user = request.user

        if logged_in_user in post.likes.all():
            # user has already liked the post
            pass
        elif logged_in_user in post.dislikes.all():
            # user has disliked the post
            post.dislikes.remove(logged_in_user)

        post.likes.add(logged_in_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='dislike')
    def dislike_post(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(post, context={
            'request': request})

        logged_in_user = request.user

        if logged_in_user in post.dislikes.all():
            # user has already disliked the post
            pass
        elif logged_in_user in post.likes.all():
            # user has liked the post
            post.likes.remove(logged_in_user)

        post.dislikes.add(logged_in_user)

        return Response(serializer.data, status=status.HTTP_200_OK)
