from rest_framework import routers

from scrap.models import Messege
from .serializers import QuoteSerializer
from .views import QuotasViewSet, MessageViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('quote', QuotasViewSet)
router.register('message', MessageViewSet, basename=Messege)


app_name = "fin_api"

urlpatterns = [path('', include(router.urls))]
