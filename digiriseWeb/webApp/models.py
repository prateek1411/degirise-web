import os
import uuid
from itertools import chain

from django.db import models

STACK_TYPE_CHOICES = [('infra', 'infra'), ('application', 'application')]


class PrintableModel(models.Model):

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(self)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(self)]
        return data

    class Meta:
        abstract = True


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


class Blueprint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blueprint = models.CharField(max_length=255, unique=True)
    blueprint_type = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_short_name(self):
        if len(self.blueprint.name) > 10:
            return self.blueprint.name[:9]
        else:
            return self.blueprint.name


class Deployment(PrintableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployment = models.CharField(max_length=255, unique=True)
    deployment_type = models.CharField(max_length=255, blank=True)
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    deployment_variables = models.JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_short_name(self):
        if len(self.deployment.name) > 10:
            return self.deployment.name[:9]
        else:
            return self.deployment.name


class Stack(PrintableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    stack_name = models.CharField(max_length=255, blank=True)
    stack_type = models.CharField(max_length=255, blank=True, choices=STACK_TYPE_CHOICES)
    code_name = models.CharField(max_length=255, blank=True)
    code = models.JSONField(blank=True, default=dict)
    status = models.CharField(max_length=255, blank=True, default='Not Created')
    created_at = models.DateTimeField(auto_now_add=True)


class RunStack(PrintableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    run_status = models.CharField(max_length=255, blank=True, default='Not Created')
    created_at = models.DateTimeField(auto_now_add=True)
