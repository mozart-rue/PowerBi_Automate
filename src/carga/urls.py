from django.urls import path, include
from .views import hometeste

urlpatterns = [
    path('', hometeste.as_view())
]