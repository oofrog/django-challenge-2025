from rest_framework import serializers
from users.serializers import TinyUserSerializer


class TweetSerializer(serializers.Serializer):

    pk = serializers.IntegerField(
        read_only=True,
    )
    payload = serializers.CharField(
        max_length=180,
    )
    user = TinyUserSerializer()
