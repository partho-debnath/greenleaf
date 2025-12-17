from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include(arg="users.urls", namespace="users")),
    path("trees/", include(arg="trees.urls", namespace="trees")),
]

if settings.DEBUG is True:
    urlpatterns += static(
        prefix=settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        prefix=settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
