from rest_framework import routers

from modules.user.viewsets import UserViewSet
from modules.auth.viewsets.register import RegisterViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'auth/register', RegisterViewSet, basename='auth-register')

urlpatterns = [
    *router.urls,
]