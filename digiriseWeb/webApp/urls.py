from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from rest_framework import routers
from . import views
from .views import InfrastructureCodeView
from rest_framework.authtoken import views as authtoken_views
admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'document', views.DocumentViewSet)

urlpatterns = [
                  path('degirise/', include('django.contrib.auth.urls')),
                  path('api/v1/', include(router.urls)),
                  path('api/v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('api/v1/api-token-auth/', authtoken_views.obtain_auth_token),
                  path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
                  path('login', auth_views.LoginView.as_view(), name='login'),
                  path('logout', auth_views.LogoutView.as_view(), name='logout'),
                  path('signup', views.signup, name='signup'),
                  path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('upload', views.file_upload, name='upload'),
                  path('', views.index, name='index'),
                  path('about_us', views.about_us, name='about_us'),
                  url(r'upload_files/(?P<filepath>.*)$', views.upload_files_list, name='listfile'),
                  url(r'api/v1/gen-code/(?P<filepath>.*)$', InfrastructureCodeView().as_view(), name='stacks'),
                  url(r'api/v1/view-code/(?P<stack>.*)/(?P<code>.*)$', InfrastructureCodeView().as_view(), name='viewcode'),
                  url(r'api/v1/code/(?P<stack>.*)/(?P<command>.*)$', InfrastructureCodeView().as_view(), name='runcode'),
                  path('delete_all_files', views.delete_all_files, name='delete_all_files')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

