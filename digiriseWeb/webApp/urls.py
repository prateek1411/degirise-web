import oauth2_provider.views as oauth2_views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views
from rest_framework.authtoken import views as token_views
from rest_framework.schemas import get_schema_view

from . import views, infra_views
from .views import swagger_view

admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'document', infra_views.DocumentViewSet)
router.register(r'deployment', infra_views.DeploymentViewSet)
router.register(r'blueprint', infra_views.BlueprintViewSet)
router.register(r'stack', infra_views.StackViewSet)
router.register(r'run_stack', infra_views.RunStackViewSet)

oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
             name="authorized-token-delete"),
    ]

urlpatterns = [
                  path('degirise/', include('django.contrib.auth.urls')),
                  path('api/v1/', include(router.urls), name='router_urls'),
                  path('api/v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('login', auth_views.LoginView.as_view(), name='login'),
                  path('logout', auth_views.LogoutView.as_view(), name='logout'),
                  path('signup', views.signup, name='signup'),
                  path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('upload', views.file_upload, name='upload'),
                  path('', views.index, name='index'),
                  path('about_us', views.about_us, name='about_us'),
                  url(r'upload_files/(?P<filepath>.*)$', views.upload_files_list, name='listfile'),
                  path('delete_all_files', views.delete_all_files, name='delete_all_files'),
                  path('delete_all_deployments', infra_views.delete_all_deployments, name='delete_all_deployments'),
                  path('delete_all_blueprint', infra_views.delete_all_blueprints, name='delete_all_blueprints'),
                  url(r'^oauth/', include('social_django.urls', namespace='social')),  # new
                  # OAuth 2 endpoints:
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('api-token-auth/', token_views.obtain_auth_token)
]
urlpatterns += [
    path('openapi', swagger_view(), name='openapi-schema'),
]

urlpatterns += [
    path('api/docs', TemplateView.as_view(
        template_name='rest_framework/swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
