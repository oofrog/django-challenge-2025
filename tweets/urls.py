from django.urls import path
from .views import tweets

urlpatterns = [
    path("", tweets),
]
