from django.conf.urls import url
from django.contrib import admin
from accounts.views import login_view, signup_view, logout_view
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm

urlpatterns = [
    url('^signup/$', accounts_views.signup_view, name='signup'),
    url('^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url('^profile/$', accounts_views.view_profile, name='view_profile'),
    url('^profile/edit/$', accounts_views.edit_profile, name='edit_profile'),
    url('^login/$', auth_views.LoginView.as_view(
            template_name='accounts/login.html'), 
            name='login', kwargs={"authentication_form":UserLoginForm}
        ),
    url('^change_password/$', accounts_views.password_change, name='change_password'),
    url(r'^reset_password/$',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/reset_password.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/reset_password_subject.txt',
            ),
            name='reset_password'
        ),
    url('^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'),
            name='password_reset_done'
        ),

    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
       auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/reset_password_confirm.html'),
            name='password_reset_confirm'
        ),

    url(r'^reset_complete/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/reset_password_complete.html'),
        ),
]
