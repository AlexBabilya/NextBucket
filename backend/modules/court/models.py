from django.db import models
import uuid

from modules.abstract.models import AbstractManager

def court_directory_path(instance, filename):
    return f'court_{instance.public_id}/{filename}'

class CourtManager(models.Manager):
    pass


class Court(models.Model):
    public_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        unique=True,
        blank=False,
        null=False
    )
    name = models.CharField(
        max_length=255, 
        unique=True, 
        db_index=True, 
        blank=False, 
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=200,blank=True, null=True)
    city = models.CharField(max_length=255,blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=court_directory_path)
    latitude = models.CharField(max_length=200,blank=True, null=True)
    longitude = models.CharField(max_length=200,blank=True, null=True)
    creator = models.ForeignKey('modules_user.User', on_delete=models.CASCADE, related_name='courts_created')
    
    objects = CourtManager()
    
    def __str__(self):
        return self.name
    
    @property
    def full_location(self):
        return f'{self.address}, {self.city}, {self.region}, {self.country}'
    
    @property
    def coordinates(self):
        return f'{self.latitude}, {self.longitude}'
