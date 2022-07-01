

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lmsApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = "Library  Admin"
admin.site.site_title = "Library Admin Portal"
admin.site.index_title = "Welcome Real Library Admin Portal"
