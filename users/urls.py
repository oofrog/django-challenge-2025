from rest_framework.urls import path
from .views import UserTweets

urlpatterns = [
    path("<int:pk>/tweets", UserTweets.as_view()),
]
