from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.register import RegisterSerializer


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('post')
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        token = RefreshToken.for_user(user)
        
        return Response({
            'user': serializer.data,
            'refresh': str(token),
            'access': str(token.access_token)
        }, status=status.HTTP_201_CREATED)