from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
import jwt
from django.conf import settings
from rest_framework.reverse import reverse
from .utils import confirm_generator
from .serializers import UserRegisterSerializer, LoginSerializer, UserViewSerializer, UserViewToAdminSerializer
from rest_framework import viewsets, status, views, authentication
from rest_framework import permissions
from django.contrib.auth.models import User
from django.core.mail import send_mail


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserViewToAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class MeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserViewSerializer

    def get(self, request):
        auth_data = authentication.get_authorization_header(request)
        prefix, token = auth_data.decode('utf-8').split(' ')
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms="HS256")

        user_data = User.objects.filter(username=payload['username']).values()[0]
        if 'Products' in request.headers:
            serializer = UserViewToAdminSerializer(data=user_data)
        else:
            serializer = UserViewSerializer(data=user_data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            domain = get_current_site(request).domain
            uuid64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse('verification', kwargs={'uuid64': uuid64, 'token': confirm_generator.make_token(user)})
            activate_url = 'http://' + domain + link

            send_mail('Confirm Registration', 'You have successfully registered. '
                                              'We are very happy to welcome you to our community.'
                                              'To complete your registration, please follow this link.\n'
                      + activate_url,
                      settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

            return Response({'user': serializer.data, 'message': 'Check your email and confirm registration'},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_token = jwt.encode({'username': user.username}, settings.JWT_SECRET_KEY)
                serializer = UserViewSerializer(user)
                data = {
                    'user': serializer.data,
                    'token': auth_token
                }

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Account not verified. Check your email to confirm registrations'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Invalid credentials or account not verified'}, status=status.HTTP_401_UNAUTHORIZED)


class VerificationView(GenericAPIView):
    serializer_class = UserViewSerializer

    def get(self, request, uuid64, token):
        try:
            id = force_str(urlsafe_base64_decode(uuid64))
            user = User.objects.get(pk=id)

            if not confirm_generator.check_token(user, token):
                return Response({'detail': 'Account already verified'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()
            serializer = UserViewSerializer(user)
            return Response({'user': serializer.data, 'message': 'Account verified'}, status=status.HTTP_200_OK)

        except (DjangoUnicodeDecodeError, User.DoesNotExist) as e:
            return Response({'detail': e}, status=status.HTTP_400_BAD_REQUEST)
