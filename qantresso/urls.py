from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('adminqan3qrapp/', admin.site.urls),
    path('', include('qrapp.urls')),
]
