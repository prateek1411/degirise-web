from django.conf import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from oauth2_provider.backends import OAuth2Backend
from rest_framework import viewsets, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .digiriseApiViews import ExtView
from .forms import DeploymentForm
from .models import Document, Deployment, Stack, Blueprint, RunStack
from .serializers import DocumentSerializer, DeploymentSerializer, StackSerializer, BlueprintSerializer, \
    RunStackSerializer


@login_required(login_url='login')
def delete_all_deployments(request):
    args = Deployment.objects.all().delete()
    return render(request, 'webApp/delete_all_files.html')


class InfrastructureCodeView(ExtView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    #    renderer_classes = [TemplateHTMLRenderer]
    #    template_name = 'infrastructure_code/infrastructure_code_template.html'

    def call_api(self, request, *args, **kwargs):
        headers = {}
        if 'stack' in list(kwargs.keys()) and 'code' in list(kwargs.keys()) and kwargs['stack'] != '' and kwargs[
            'code'] != '':
            self.url = settings.API + 'viewcode/' + kwargs['stack'] + '/' + kwargs['code']
        else:
            self.url = settings.API + 'stacklist/'
        return super().call_api(request, *args, **kwargs)


class StackList(ExtView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #    authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [SessionAuthentication, OAuth2Backend]
    permission_classes = [IsAuthenticated]

    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'infrastructure_code/infrastructure_code_template.html'

    def call_api(self, request, *args, **kwargs):

        headers = {}
        if 'filepath' in list(kwargs.keys()) and kwargs['filepath'] != '':
            self.url = settings.API + 'stack-file-list/' + kwargs['filepath']
        else:
            self.url = settings.API + 'stacklist/'

        response = super().call_api(request, *args, **kwargs)
        return Response({'stacks': response.data})


class CreateStack(ExtView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'infrastructure_code/infrastructure_code_template.html'
    queryset = Deployment.objects.all()
    headers = {'content-type': 'application/json'}

    def call_api(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                blueprint = get_object_or_404(Blueprint, blueprint='my_blueprint')
            except Http404 as http_error:
                blueprint = Blueprint().objects.create(deployment='my_blueprint', description="first Blueprint")
            try:
                deployment = get_object_or_404(Deployment, deployment='Test')
            except Http404 as http_error:
                deployment = Deployment().objects.create(blueprint=blueprint, deployment='Test',
                                                         description="first Deployment")

            self.url = settings.API + 'generate/'

            response = super().call_api(request, headers=self.headers, *args, **kwargs)

            stack = Stack()
            stack.deployment = deployment
            stack_list = StackList().call_api(request)
            if len(stack_list.data['stacks']) != 0:
                for (k, v) in stack_list.data['stacks'].items():
                    for values in v:
                        try:
                            stack = get_object_or_404(Stack, deployment=deployment, stack_name=k, code_name=values)
                        except Http404:
                            stack = Stack.objects.create(deployment=deployment, stack_name=k, code_name=values)
                        stack.code = InfrastructureCodeView().call_api(request, stack=k, code=values).data
                        stack.save()
            return Response({'stacks': response.data})
        else:
            queryset = Deployment.objects.all()
            return render({'deployments': queryset})


class DeploymentView(generic.CreateView):
    form_class = DeploymentForm
    success_url = reverse_lazy('index')
    template_name = 'infrastructure_code/infrastructure_code_template.html'


class RunStackAPI(ExtView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'infrastructure_code/infrastructure_code_template.html'

    def call_api(self, request, *args, **kwargs):

        headers = {}
        if 'stack' in list(kwargs.keys()):
            self.url = settings.API + 'code/' + kwargs['stack'] + '/' + kwargs['command']
        else:
            print("Not a valid URL")
            return Response({'stacks-run': 'failure'})
        deployment = Deployment()
        try:
            deployment = get_object_or_404(Deployment, deployment='Test')
        except Http404 as http_error:
            print("stack does not exist")
            return Response({'stacks-run': 'failure'})
        stack = Stack()
        stack.deployment = deployment
        stack_list = StackList().call_api(request)
        if len(stack_list.data['stacks']) != 0:
            for (k, v) in stack_list.data['stacks'].items():
                for values in v:
                    try:
                        stack = get_object_or_404(Stack, deployment=deployment, stack_name=k, code_name=values)
                    except Http404:
                        print("stack does not exist")
                        return Response({'stacks-run': 'failure'})
                    response = super().call_api(request, *args, **kwargs)
                    stack.status = kwargs['command']
                    stack.save()
        return Response({'stack-run': response.data})


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('document')
    serializer_class = DocumentSerializer


class DeploymentViewSet(viewsets.ModelViewSet):
    queryset = Deployment.objects.all().order_by('deployment')
    serializer_class = DeploymentSerializer


class BlueprintViewSet(viewsets.ModelViewSet):
    queryset = Blueprint.objects.all().order_by('deployment')
    serializer_class = BlueprintSerializer


class StackViewSet(viewsets.ModelViewSet):
    queryset = Stack.objects.all().order_by('deployment')
    serializer_class = StackSerializer


class StackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stack.objects.all()
    serializer_class = StackSerializer


class RunStackViewSet(viewsets.ModelViewSet):
    queryset = RunStack.objects.all().order_by('created_at')
    serializer_class = RunStackSerializer
