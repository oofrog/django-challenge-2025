from rest_framework.serializers import ModelSerializer
from .models import Tweet
from users.serializers import TinyUserSerializer


class TweetSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = "__all__"
