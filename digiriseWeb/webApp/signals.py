from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404

from .digiriseApiViews import ExtView
from .models import Deployment, Blueprint, Stack, RunStack


@receiver(pre_save, sender=Deployment)
def before_saving_deployment(sender, instance: Deployment, *args, **kwargs):
    headers = {}
    try:
        blueprint = get_object_or_404(Blueprint, blueprint=instance.blueprint.id)
    except Http404 as http_error:
        print('Blueprint not found')
    data = instance.to_dict()
    data['blueprint'] = instance.blueprint.blueprint
    print(data)

    req = CallApiRequest(method='post', data=data)
    ext_view = ExtView()
    ext_view.url = settings.API + 'generate/'
    response = ext_view.call_api(req, headers=headers, *args, **kwargs)
    if not response.data['stack_created']:
        print('stack code not generated. Check the Infrastructure service')
        exit(1)


@receiver(post_save, sender=Deployment)
def after_saving_deployment(sender, instance: Deployment, *args, **kwargs):
    headers = {}
    for ext_api in ('application', 'infra'):
        ext_view = ExtView()
        ext_view.url = '{0}{1}-stack-list/{2}/{3}'.format(settings.API, ext_api, instance.blueprint.blueprint,
                                                          instance.deployment)
        req = CallApiRequest(method='get')

        response = ext_view.call_api(req, headers=headers, *args, **kwargs)
        for (k, v) in response.data['code'].items():
            stack = Stack()
            stack.deployment = instance
            stack.stack_name = k
            if ext_api == 'infra':
                stack.code = v['cdk.tf.json']
                stack.code_name = 'terraform'
            else:
                stack.code = v
                stack.code_name = 'kubernetes'
            stack.stack_type = ext_api
            stack.save()


@receiver(pre_save, sender=RunStack)
def before_saving_runstack(sender, instance: RunStack, *args, **kwargs):
    headers = {}

    try:
        query_set = Stack.objects.filter(deployment=instance.deployment.id).order_by('-stack_type')
    except Http404 as http_error:
        print('Stack code not generate. First generate the code')
        exit(1)
    else:
        for stack in query_set.iterator():
            data = stack.to_dict()
            data.update({'command': instance.command, 'blueprint': instance.blueprint.blueprint})
            data['deployment'] = instance.deployment.deployment
            data.pop('created_at', None)
            data.pop('code', None)
            req = CallApiRequest(method='post', data=data)
            ext_view = ExtView()
            ext_view.url = '{0}{1}-code'.format(settings.API, stack.stack_type)
            response = ext_view.call_api(req, headers=headers, *args, **kwargs)
        # if not response.data['stack_created']:
        #    print('stack code not generated. Check the Infrastructure service')
        #    exit(1)


class CallApiRequest:
    def __init__(self, method, data=None):
        if data is None:
            data = {}
        self.method = method
        self.data = data


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
