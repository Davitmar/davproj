from django.urls import path, include, reverse_lazy
from .views import RegisterUser, LoginUser, user_logout, settings
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [path('register', RegisterUser.as_view(), name='register'),
               path('login', LoginUser.as_view(), name='login'),
               path('logout', user_logout, name='logout'),
               path('settings', settings, name='settings'),
               path('password_change', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done')), name='password_change'),
               path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
               path('password_reset', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),#email_template_name='registration/password_reset_email.html'
               path('password_reset_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
               path('password/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')),
                    name='password_reset_confirm'),
               path('password/reset/done', auth_views.PasswordResetCompleteView.as_view(),
                    name='password_reset_complete')]

