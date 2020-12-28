from abc import ABC

from rest_framework import serializers

from .models import Document, Deployment, Stack, Blueprint, RunStack


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('document', 'uploaded_at')


class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = ('blueprint', 'deployment', 'deployment_type', 'deployment_variables', 'description')


class BlueprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blueprint
        fields = ('blueprint', 'blueprint_type', 'description','created_at')


class StackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stack
        fields = ('deployment', 'stack_name', 'stack_type', 'code_name', 'code', 'status','created_at')

class RunStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunStack
        fields = ('deployment', 'blueprint', 'stack_name', 'stack_type', 'command', 'run_status','created_at')