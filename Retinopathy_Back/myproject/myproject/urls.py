from django.contrib import admin
from django.urls import path
from api.views import process_image


urlpatterns = [
    path('admin/', admin.site.urls),
    path('process_image/', process_image, name='process_image'),
]
