import os

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from rest_framework.fields import JSONField


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='.')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_extension(self):
        name, extension = os.path.splitext(self.document.name)
        return extension

    def get_short_name(self):
        if len(self.document.name) > 10:
            return self.document.name[:9]
        else:
            return self.document.name


class Deployment(models.Model):
    deployment = models.CharField(max_length=255,unique=True)
    description = models.CharField(max_length=255,blank=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def get_short_name(self):
        if len(self.deployment.name) > 10:
            return self.deployment.name[:9]
        else:
            return self.deployment.name


class Stack(models.Model):
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    stack_name = models.CharField(max_length=255,blank=True)
    code_name = models.CharField(max_length=255,blank=True)
    code = models.JSONField(blank=True,default=dict)
    status = models.CharField(max_length=255, blank=True,default='Not Created')
