from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('', include('socialmediawebsite.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
