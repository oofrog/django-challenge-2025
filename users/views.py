from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
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

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = PublicUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PublicUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


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


class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "hello"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye"})


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_pw = request.data.get("old_password")
        new_pw = request.data.get("new_password")
        if not old_pw or not new_pw:
            raise ParseError
        if user.check_password(old_pw):
            user.set_password(new_pw)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
