from tempfile import template
from django.urls import path
from .views import Verification
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static


app_name = 'authentication'


urlpatterns = [
    path('account/type/', TemplateView.as_view(template_name='authentication/index.html'), name='index'),
    path('register/',views.register, name="register"),
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('social_auth/<str:name>',views.social_auth, name="social_auth"),
    path('logout/',auth_view.LogoutView.as_view(),name='logout'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('verify_email/',
        TemplateView.as_view(template_name='authentication/verify-email.html'), 
        name='verify_email'),
    path('verify_admin/',
        TemplateView.as_view(template_name='authentication/verify-admin.html'),
        name='verify_admin'),
    path('welcome',
        TemplateView.as_view(template_name='authentication/welcome.html'),
        name='welcome'),
    path('activate/<uidb64>/<token>/<email>',Verification.as_view(),name='activate'),
    path('corporate-success/',
        TemplateView.as_view(template_name='authentication/corporate-success.html'),
        name="corporate-success"),
    path('accounts/social/signup/',
        TemplateView.as_view(template_name='authentication/google-email-exist.html'),
        name="google-email-exists"),
    path('new-password/<slug:token>/<str:type>/',views.new_password,name="new-password"),
    path('account-inactive/',
        TemplateView.as_view(template_name='authentication/account-inactive.html'),
        name="account-inactive"),
    path('accounts/profile/',views.google_login,name="google-login"),
    path('change-mode/',views.changemode,name='change-mode'),
    path('send-mail-password/', views.send_mail_password, name='send_mail_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
