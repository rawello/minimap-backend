from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    login = models.CharField(max_length=250, null=False, unique=True)
    password = models.CharField(max_length=250, null=False)

class Maps(models.Model):
    svg = models.JSONField(null=False)
    rooms = models.JSONField(null=False)
    login = models.CharField(max_length=250, null=False)
    build = models.CharField(max_length=250, null=False, unique=True)