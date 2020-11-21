from django.http import request
import jwt

from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse

from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, GoogleSocialAuthSerializer
from .models import User
from .renderers import UserRenderer

from .utils import Util


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

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

    serializer_class = EmailVerificationSerializer
    renderer_classes = (UserRenderer,)

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Successfully Activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Link Expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error': 'Unknown Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # TODO: Handle Exceptions of invalid credentials - Authentication Failed
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        """
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = (serializer.validated_data)

        return Response(data, status=status.HTTP_200_OK)
