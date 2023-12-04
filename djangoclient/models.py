from django.db import models
from django.core.validators import int_list_validator

class User(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    login = models.CharField(max_length=250, null=False, unique=True)
    password = models.CharField(max_length=250, null=False)

class Maps(models.Model):
    svg = models.JSONField(null=False)
    rooms = models.JSONField(null=False)
    obj = models.JSONField(null=False, default="default")
    login = models.CharField(max_length=250, null=False)
    build = models.CharField(max_length=250, null=False, unique=True)
    floors = models.CharField(validators=[int_list_validator], max_length=100, null=False, default=[1])

# class FrontObj(models.Model):
#     login = models.CharField(max_length=250, null=False, default="default")
#     build = models.CharField(max_length=250, null=False, unique=True, default="default")
