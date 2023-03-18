from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
from django.conf import settings


class Authentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None

        try:

            user = User(username=payload['username'])
            return user, token
        except jwt.DecodeError as error:
            raise exceptions.AuthenticationFailed('Your token is invalid, login')
        except jwt.ExpiredSignatureError as error:
            raise exceptions.AuthenticationFailed('Your token is expired, login')
        except User.DoesNotExist as error:
            raise exceptions.NotAuthenticated('This user does not exist, register')