from rest_framework import routers
from .viewsets import PostListViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostListViewSet)
