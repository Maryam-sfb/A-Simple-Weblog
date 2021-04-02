
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myblog.urls', namespace='myblog')),
    path('', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('ckeditor_upload/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
