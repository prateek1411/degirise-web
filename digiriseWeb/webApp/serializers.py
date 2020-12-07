from abc import ABC

from rest_framework import serializers

from .models import Document, Deployment, Stack


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('document', 'uploaded_at')


class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = ('deployment', 'description')


class StackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = ('deployment', 'stack_name', 'code_name', 'code', 'status')
