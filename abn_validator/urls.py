from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from data_analyser.views import upload_file, data_preview, results

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_file),
    path('data_preview/', data_preview),
    path('results/', results),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
