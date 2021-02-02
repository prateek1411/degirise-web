import itertools
from datetime import datetime, timedelta

from oauth2_provider.backends import OAuth2Backend
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from azure.storage.blob import BlockBlobService, ContainerPermissions
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets, generics, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from .digiriseApiViews import ExtView
from .forms import DocumentForm
from .models import Document, Deployment, Stack, Blueprint
from .serializers import DocumentSerializer, DeploymentSerializer, StackSerializer


def get_sas_token():
    blobService = BlockBlobService(account_name=settings.AZURE_ACCOUNT_NAME, account_key=settings.AZURE_ACCOUNT_KEY)
    sas_token = blobService.generate_container_shared_access_signature(settings.MEDIA_CONTAINER,
                                                                       ContainerPermissions.READ,
                                                                       datetime.utcnow() + timedelta(hours=1))
    # print url
    return sas_token


def index(request):
    return render(request, 'webApp/index.html')


def about_us(request):
    return render(request, 'webApp/about_us.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})


@ensure_csrf_cookie
def signout(request):
    logout(request)
    return redirect('/')


def email_check(user):
    return user.email.endswith('@example.com')


@login_required(login_url='login')
@permission_required('webApp.add_document')
def file_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            resp = form.save()
            document_name = resp.document
            args = Document.objects.get(document=document_name)
            sas_token = get_sas_token()
            args = {'uploaded_file': args, 'sas_token': sas_token}
            return render(request, 'webApp/upload.html', args)
    else:
        form = DocumentForm()
    return render(request, 'webApp/upload.html', {
        'form': form
    })


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/signup.html'


class UploadView(generic.CreateView):
    form_class = DocumentForm
    success_url = reverse_lazy('index')
    template_name = 'webApp/model_form_upload.html'


@login_required(login_url='login')
@permission_required('webApp.view_document')
def upload_files_list(request, filepath):
    args = Document.objects.all()
    result = [[v for v in itertools.islice(args, start, start + 5)] for start in range(0, len(args), 5)]
    sas_token = get_sas_token()
    return render(request, 'webApp/upload_list.html', {"doc_list": result, "sas_token": sas_token})


@login_required(login_url='login')
def delete_all_files(request):
    args = Document.objects.all().delete()
    return render(request, 'webApp/delete_all_files.html')


def swagger_view():
    return get_schema_view(
        title="Digirise AB",
        description="Digirise API Documentation",
        version="1.0.0"
    )
