"""
URL configuration for daily_puzzle project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/puzzles/', include('puzzles.urls')),
    path('api/users/', include('users.urls')),
    path('api/validators/', include('validators.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)