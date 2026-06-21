from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from micro_cms.admin import owner_admin_site
from public.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("owner/", owner_admin_site.urls),
    path("summernote/", include("django_summernote.urls")),
    path("", home, name="home"),
    path("<slug:slug>/", home, name="home_slug"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
