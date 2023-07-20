from rest_framework import serializers

from modules.user.models import User
from modules.user.serializers import UserSerializer


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(
        max_length=128, 
        min_length=8, 
        required=True, 
        write_only=True
    )
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    class Meta:
        model = User
        fields = [
            'public_id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'height',
            'weight',
            'gender',
            'position',
            'city',
            'region',
            'country',
            'bio',
            'avatar',
        ]
