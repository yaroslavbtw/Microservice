from django.urls import path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', UsersViewSet)

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('verification/<uuid64>/<token>/', VerificationView.as_view(), name='verification'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
]

urlpatterns += router.urls
