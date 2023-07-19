from rest_framework import routers

from modules.user.viewsets import UserViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    *router.urls,
]