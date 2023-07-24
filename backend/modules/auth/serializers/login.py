from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, ValidationError
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from modules.user.serializers import UserSerializer

User = get_user_model()


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        self.user = None
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            self.user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if self.user is None:
                try:
                    self.user = User.objects.get(email=username)
                    self.user.check_password(password) 
                except User.DoesNotExist:
                    pass
        
        if not self.user:
            raise ValidationError('Unable to log in with provided credentials.')
        
        refresh = self.get_token(self.user)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
  
        return {
            "user": UserSerializer(self.user, context=self.context).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }