from django.contrib import admin
from django.urls import path, include
from catalog.views import index, successful_registration
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from registration.views import signup, email_confirm_url, enter_email_confirm_code
from django.conf.urls.i18n import i18n_patterns

urlpatterns = []

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/reset/done', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
    path('accounts/reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path('accounts/password_reset/', PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        subject_template_name='registration/password_reset_subject.txt',
        email_template_name='registration/password_reset_email.html'),
        name='password_reset'),
    path('accounts/password_change/', PasswordChangeView.as_view(
        template_name='registration/password_change_form.html'),
        name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),
    path('accounts/login', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),
    path('accounts/email-confirm-page/<uuid:token>/', email_confirm_url, name='email-link-confirm-page'),
    path('accounts/enter-email-confirm-code/', enter_email_confirm_code, name='email-confirm-page'),
    path('catalog/', include('catalog.urls')),
    path('payment/', include('payment.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('information/', include('information.urls')),
    path('crons/', include('crons.urls')),
    path('', index, name='index'),
    path('accounts/registration/', signup, name='signup'),
    path('accounts/registration/successful/', successful_registration, name='successful_registration'),
    path('admin/', admin.site.urls),


)
