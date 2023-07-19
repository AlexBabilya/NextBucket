import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from ..abstract.models import AbstractManager

POSITION_CHOICES= [
    ('NO', 'Not Selected'),
    ('PG', 'Point Guard'),
    ('SG', 'Shooting Guard'),
    ('SF', 'Small Forward'),
    ('PF', 'Power Forward'),
    ('C', 'Center'),
]

def user_directory_path(instance, filename):
    return f'user_{instance.public_id}/{filename}'


class UserManager(BaseUserManager, AbstractManager):
    pass


class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        unique=True,
        blank=False,
        null=False
    )
    username = models.CharField(
        max_length=255, 
        unique=True, 
        db_index=True, 
        editable=False, 
        blank=False, 
        null=False
    )
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    height = models.DecimalField(max_digits=4, decimal_places=1)
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0])
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    
    EMAIL_FILED = 'email'
    USERNAME_FIELD = 'username'
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    


