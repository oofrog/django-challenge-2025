from rest_framework.urls import path
from .views import user_tweets

urlpatterns = [
    path("<int:pk>/tweets", user_tweets),
]
