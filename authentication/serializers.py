import os

from django.db.models.expressions import Value
from django.http import request
from django.contrib import auth

from rest_framework import serializers

from google.oauth2 import id_token
from google.auth.transport import Request, requests

from .models import User
from .register import register_social_user


MAX_PASSWORD_LENGTH = 68
MIN_PASSWORD_LENGTH = 8


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=MAX_PASSWORD_LENGTH, min_length=MIN_PASSWORD_LENGTH, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password',
                  'phone_number', 'profession')

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        phone_number = attrs.get('phone_number', '0000000000')
        profession = attrs.get('profession', 'Unemployed')

        # TODO: Validate Password using regexs

        if not username.isalnum():
            raise serializers.ValidationError(
                'Username must contain only alphanumeric characters')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(
        max_length=MAX_PASSWORD_LENGTH, min_length=MIN_PASSWORD_LENGTH, write_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password',
                  'phone_number', 'profession', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise serializers.AuthenticationFailed(
                'Invalid Credentials, try again.'
            )

        if not user.is_active:
            raise serializers.AuthenticationFailed(
                'Account Disabled. Contact admin'
            )

        if not user.is_verified:
            raise serializers.AuthenticationFailed(
                'Email Not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens(),
        }

        return super().validate(attrs)


class GoogleSocialAuthSerializer(serializers.Serializer):
    token = serializers.CharField()

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

    def validate_auth_token(self, auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request(), self.GOOGLE_CLIENT_ID)
        except ValueError:
            raise serializers.AuthenticationFailed(
                'Invalid Token. Try again'
            )

        userid = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']

        return register_social_user(
            provider='google', user_id=userid, email=email, name=name
        )
