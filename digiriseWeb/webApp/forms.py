from django import forms

from .models import Document, Deployment, Blueprint, Stack


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document',)

class DeploymentForm(forms.ModelForm):
    class Meta:
        model = Deployment
        fields = ('blueprint', 'deployment', 'deployment_type', 'deployment_variables', 'description')


class BlueprintForm(forms.ModelForm):
    class Meta:
        model = Blueprint
        fields = ('blueprint', 'blueprint_type', 'description')


class StackForm(forms.ModelForm):
    class Meta:
        model = Stack
        fields = ('deployment', 'stack_name', 'code_name', 'code', 'status')
