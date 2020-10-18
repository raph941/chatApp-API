from rest_framework import serializers
from accounts.models import User


class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    initials = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'fullname', 'email', 'initials', 'password')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=False)
    initials = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'fullname', 'email', 'initials', 'password')