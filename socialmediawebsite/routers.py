from rest_framework import routers
from .viewsets import PostViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
