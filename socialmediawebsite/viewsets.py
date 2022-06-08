from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    queryset = Post.objects.all()

    def list(self, request):
        serializer = PostSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(user)
        return Response(serializer.data)
