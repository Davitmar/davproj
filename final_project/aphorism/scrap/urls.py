from django.urls import path
from .views import AphListView, AphView, AddAph, UpdateAph, DeleteAph
from django.contrib.auth.decorators import login_required

app_name = 'scrap'
urlpatterns = [path('', AphListView.as_view(), name='get_aphs'),
               path('add', AddAph.as_view(), name='add'),
               path('update/<pk>', login_required(UpdateAph.as_view()), name='update'),
               path('delete/<pk>', login_required(DeleteAph.as_view()), name='delete'),
               path('<pk>', AphView.as_view(), name='aph')]
