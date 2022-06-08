from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    http_method_names = ['get', 'post']

    def list(self, request):
        serializer = PostSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='like')
    def like_post(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(post)

        logged_in_user = request.user

        if logged_in_user in post.likes.all():
            #user has already liked the post
            pass
        elif logged_in_user in post.dislikes.all():
            #user has disliked the post
            post.dislikes.remove(logged_in_user)

        post.likes.add(logged_in_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='dislike')
    def dislike_post(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(post)

        logged_in_user = request.user

        if logged_in_user in post.dislikes.all():
            #user has already disliked the post
            pass
        elif logged_in_user in post.likes.all():
            #user has liked the post
            post.likes.remove(logged_in_user)

        post.dislikes.add(logged_in_user)

        return Response(serializer.data, status=status.HTTP_200_OK)
