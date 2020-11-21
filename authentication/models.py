import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
from django.core.validators import RegexValidator

from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, password, phone_number="000000000", profession="Unemployed"):

        if username is None:
            raise TypeError('Users must have a Username')

        if email is None:
            raise TypeError('Users must have an Email ID')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
            profession=profession
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Password should not be None')

        user = self.create_user(username, email, password, "00000000", "Admin")
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


AUTH_PROVIDERS = {"facebook": "facebook",
                  "google": "google", "email": "emails"}


class User(AbstractBaseUser, PermissionsMixin):

    phone_number_regex = RegexValidator(regex=r'^\+?[0-9]{9,15}$')

    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.CharField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(max_length=15, validators=[
                                    phone_number_regex], default='0000000000')
    profession = models.CharField(max_length=255, default="Unemployed")
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email')
    )

    # TODO: Validate username using regex (On Frontend)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
        # return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
