from django.urls import path

from .views import RegisterView, VerifyEmail, GoogleSocialAuthView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('google-auth/', GoogleSocialAuthView.as_view(), name='verify'),
]
