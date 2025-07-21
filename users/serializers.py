from rest_framework.serializers import ModelSerializer
from .models import User


class TinyUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
        )


class PublicUserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = (
            "password",
            "last_login",
            "is_superuser",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",  
            "user_permissions",
        )
