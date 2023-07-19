from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        try:
            return self.get(public_id=public_id)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404
                
    class Meta:
        abstract = True