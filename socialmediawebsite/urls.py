from django.urls import path, include

from .routers import router
from .views import PostListView


urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
]

urlpatterns += [
    path('api/', include(router.urls))
]