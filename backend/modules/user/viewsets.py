from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from serializers import UserSerializer
from models import User

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('get', 'patch')
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        
        if self.request.user.is_staff:
            return User.objects.exclude(is_superuser=True)
        
        return User.objects.exclude(is_superuser=True, is_staff=True)    
    
