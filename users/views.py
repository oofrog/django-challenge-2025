from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import User
from .serializers import TinyUserSerializer, PublicUserSerializer
from tweets.models import Tweet
from tweets.serializers import TweetSerializer


class UserTweets(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user = self.get_object(pk)
        tweets = Tweet.objects.filter(user=user)
        serializer = TweetSerializer(
            tweets,
            many=True,
        )
        return Response(serializer.data)


class Users(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = TinyUserSerializer(
            users,
            many=True,
        )
        return Response(serializer.data)


class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)
