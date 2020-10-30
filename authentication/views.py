from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, GoogleSocialAuthSerializer
from .models import User

from .utils import Util


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')

        absolute_url = f'http://{current_site}{relative_link}?token={token}'

        email_body = f'Hi {user.username}!\nUse the link to verify your email\n{absolute_url}'

        data = {
            'to_email': [user.email],
            'email_body': email_body,
            'email_subject': 'Verify your email',
        }

        Util.send_email(data=data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        pass


class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])

        return Response(data, status=status.HTTP_200_OK)
