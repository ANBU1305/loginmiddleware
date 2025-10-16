# authentication_api/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserLogin

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = ('name', 'email', 'address', 'hobbies')

class UserSerializerWithProfile(serializers.ModelSerializer):
    userlogin = UserLoginSerializer(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'userlogin')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        userlogin_data = validated_data.pop('userlogin')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        UserLogin.objects.create(user=user, **userlogin_data)
        return user