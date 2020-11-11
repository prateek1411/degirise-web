from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.static import serve

from . import views

urlpatterns = [
                  path('degirise/', include('django.contrib.auth.urls')),
                  path('login', auth_views.LoginView.as_view(), name='login'),
                  path('logout', auth_views.LogoutView.as_view(), name='logout'),
#                  path('signup', views.signup, name='signup'),
                  path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('upload', views.model_form_upload, name='upload'),
                  path('', views.index, name='index'),
                  url('upload_files/(?P<filepath>.*)$', views.upload_files_list, name='listfile'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
