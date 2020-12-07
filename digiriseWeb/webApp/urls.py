from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from rest_framework import routers
from . import views
from .views import InfrastructureCodeView, StackList, CreateStack, RunStack
from rest_framework.authtoken import views as authtoken_views
import oauth2_provider.views as oauth2_views

admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'document', views.DocumentViewSet)
router.register(r'deployment', views.DeploymentViewSet)
router.register(r'stack', views.StackViewSet)

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
                  path('api/v1/', include(router.urls)),
                  path('api/v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('api/v1/api-token-auth/', authtoken_views.obtain_auth_token),
                  path('login', auth_views.LoginView.as_view(), name='login'),
                  path('logout', auth_views.LogoutView.as_view(), name='logout'),
                  path('signup', views.signup, name='signup'),
                  path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('upload', views.file_upload, name='upload'),
                  path('', views.index, name='index'),
                  path('about_us', views.about_us, name='about_us'),
                  url(r'upload_files/(?P<filepath>.*)$', views.upload_files_list, name='listfile'),
                  url(r'api/v1/generate-stack-code/(?P<deployment_name>.*)$', CreateStack().as_view(), name='stacks'),
                  url(r'api/v1/stack-list/(?P<filepath>.*)$', StackList().as_view(), name='stacks'),
                  url(r'api/v1/view-code/(?P<stack>.*)/(?P<code>.*)$', InfrastructureCodeView().as_view(), name='viewcode'),
                  url(r'api/v1/code/(?P<stack>.*)/(?P<command>.*)$', RunStack().as_view(), name='runcode'),
                  path('delete_all_files', views.delete_all_files, name='delete_all_files'),
                  path('delete_all_deployments', views.delete_all_deployments, name='delete_all_deployments'),
                  # OAuth 2 endpoints:
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

