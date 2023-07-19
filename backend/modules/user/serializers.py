from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SlugRelatedField(many=True, slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(many=True, slug_field='username', read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
    
    class Meta:
        model = User
        fields = [
            'public_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'created_at',
            'updated_at',
            'is_active',
            'height',
            'weight',
            'gender',
            'position',
            'city',
            'region',
            'country',
            'bio',
            'avatar',
            'followers',
            'following',
            'followers_count',
            'following_count',
        ]
        read_only_fields = [
            'public_id',
            'username',
            'email',
            'created_at',
            'updated_at',
            'followers',
            'following',
        ]

