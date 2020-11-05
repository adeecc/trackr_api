from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import RegisterView, VerifyEmail, LoginAPIView, GoogleSocialAuthView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name=''),
    path('google-auth/', GoogleSocialAuthView.as_view(), name='verify'),
]
