from django.contrib import admin
from django.urls import path
from api.views import model_inference


urlpatterns = [
    path('admin/', admin.site.urls),
    path('process_image/', model_inference, name='model_inference'),
]
