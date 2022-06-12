from django.urls import path
from .views import AphListView, AphView, AddAph, UpdateAph, DeleteAph, fav_add, SendMes, Sentes, Sms, DeleteMes, \
    UsersList, UserDelete, UserView, UserUpdate, AddPhoto, set_main, delete_photo, friend_send, friend_requests, \
    friend_response, friend_reject
from django.contrib.auth.decorators import login_required

app_name = 'scrap'
urlpatterns = [path('', AphListView.as_view(), name='get_aphs'),
               path('mess', login_required(SendMes.as_view()), name='mess'),
               path('sent', login_required(Sentes.as_view()), name='sent'),
               path('sms', Sms.as_view(), name='sms'),
               path('delete_mes/<pk>', DeleteMes.as_view(), name='delete_mes'),
               path('add', AddAph.as_view(), name='add'),
               path('update/<pk>', login_required(UpdateAph.as_view()), name='update'),
               path('delete/<pk>', login_required(DeleteAph.as_view()), name='delete'),
               path('/<pk>', AphView.as_view(), name='aph'),
               path('fav/<i>', login_required(fav_add), name='fav_add'),
               path('users_list', login_required(UsersList.as_view()), name='users_list'),
               path('user_update/<pk>', login_required(UserUpdate.as_view()), name='user_update'),
               path('user_delete/<pk>', login_required(UserDelete.as_view()), name='user_delete'),
               path('users_list/<pk>', login_required(UserView.as_view()), name='user_view'),
               path('add_photo', login_required(AddPhoto.as_view()), name='add_photo'),
               path('set_main/<j>', login_required(set_main), name='set_main'),
               path('delete_photo/<i>', login_required(delete_photo), name='delete_photo'),
               path('friend_send/<i>', login_required(friend_send), name='friend_send'),
               path('friend_requests', login_required(friend_requests), name='friend_requests'),
               path('friend_response/<i>', login_required(friend_response), name='friend_response'),
               path('friend_reject/<i>', login_required(friend_reject), name='friend_reject')
               ]
