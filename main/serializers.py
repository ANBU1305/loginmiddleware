# authentication_api/serializers.py

from rest_framework import serializers
from .models import User, UserLogin

class UserLoginSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    address = serializers.DictField()
    hobbies = serializers.ListField(child=serializers.CharField())

class UserSerializerWithProfile(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    userlogin = UserLoginSerializer()

    def create(self, validated_data):
        userlogin_data = validated_data.pop('userlogin')

        # Create MongoEngine User document
        user = User(**validated_data).save()

        # Create related UserLogin profile
        UserLogin(user=user, **userlogin_data).save()

        return user
