from django.urls import path,include
from .views import RegisterUser, LoginUser, user_logout


app_name = 'user_auth'
urlpatterns = [path('register', RegisterUser.as_view(), name='register'),
               path('login', LoginUser.as_view(), name='login'),
               path('logout', user_logout, name='logout')]

