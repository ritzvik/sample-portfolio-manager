from django.db import models

from code_service.core.abstract_models import BigIDAbstract

# Create your models here.


class UserProfile(BigIDAbstract):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, db_index=True)
