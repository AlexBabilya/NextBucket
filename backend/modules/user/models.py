import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from modules.abstract.models import AbstractManager

POSITION_CHOICES= [
    ('NO', 'Not Selected'),
    ('PG', 'Point Guard'),
    ('SG', 'Shooting Guard'),
    ('SF', 'Small Forward'),
    ('PF', 'Power Forward'),
    ('C', 'Center'),
]

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

def user_directory_path(instance, filename):
    return f'user_{instance.public_id}/{filename}'


class UserManager(BaseUserManager, AbstractManager):
    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError('Users must have a username')
        if email is None:
            raise TypeError('Users must have an email')
        if password is None:
            raise TypeError('Users must have a password')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_stuff(self, username, email, password=None, **kwargs):
        user = self.create_user(username, email, password, **kwargs)
        
        user.is_staff = True
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, email, password, **kwargs):
        user = self.create_stuff(username, email, password, **kwargs)
        
        user.is_superuser = True
        user.save(using=self._db)
        
        return user           
        

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
        blank=False, 
        null=False
    )
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=254, unique=True, db_index=True, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    weight = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0])
    city = models.CharField(max_length=255,blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    courts_liked = models.ManyToManyField('modules_court.Court', related_name='liked_by')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=True, null=True)
    
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def follow_user(self, user):
        return self.followers.add(user)    
    
    def remove_followed_user(self, user):
        return self.followers.remove(user)
    
    def has_followed_user(self, user):
        return self.followers.filter(pk=user.pk).exists()
    
    def like_court(self, court):
        return self.courts_liked.add(court)    
    
    def remove_liked_court(self, court):
        return self.courts_liked.remove(court)
    
    def has_liked_court(self, court):
        return self.courts_liked.filter(pk=court.pk).exists()

    