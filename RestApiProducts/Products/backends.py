from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
from rest_framework.request import HttpRequest
import requests


class JwtAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None

        try:
            response = requests.get("http://localhost:85/api/v1/users/me", headers={"Authorization": auth_data,
                                                                                    "Products": 'True'})
            prefix, token = auth_data.decode('utf-8').split(' ')
            data = response.json()
            user = User(username=data['username'], email=data['email'], is_superuser=data['is_superuser'],
                        is_staff=data['is_staff'], is_active=data['is_active'])
            print(response.status)
            return user, token
        except requests.exceptions.ConnectionError as err:
            print("Error")
