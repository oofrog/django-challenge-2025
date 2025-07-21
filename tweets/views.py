from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from .models import Tweet
from .serializers import TweetSerializer


class Tweets(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(
            tweets,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            new_tweet = serializer.save(user=request.user)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TweetDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        tweet = self.get_object(pk)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data)

    def put(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.user != request.user:
            raise PermissionDenied
        serializer = TweetSerializer(
            tweet,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_tweet = serializer.save()
            serializer = TweetSerializer(updated_tweet)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.user != request.user:
            raise PermissionDenied
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    