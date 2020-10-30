from django.contrib.auth import authenticate
from authentication.models import User

import os
import random
from rest_framework.exceptions import AuthenticationFailed


def generate_username(name):

    username = "".join(name.split(' ').lower())

    if not User.objects.filter(username=username).exists():
        return username

    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)
    social_password = os.environ.get('SOCIAL_SECRET')

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=social_password)

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                # 'tokens': registered_user.token()
            }
        else:
            raise AuthenticationFailed(
                detail=f'Please Login with your {filtered_user_by_email[0].authenticate} account')
    else:
        user = {
            'username': generate_username(name),
            'email': email,
            'password': social_password
        }

        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=social_password
        )

        return {
            'username': new_user.username,
            'email': new_user.email,
            # 'tokens': new_user.token()
        }
