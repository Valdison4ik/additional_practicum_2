from django.urls import path, include

urlpatterns = [
path('config/', include('config.urls')),
]