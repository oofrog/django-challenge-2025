from rest_framework import serializers

class TinyUserSerializer(serializers.Serializer):

    pk = serializers.IntegerField(read_only=True)
    username=serializers.CharField()