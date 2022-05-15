from rest_framework import routers
from .serializers import QuoteSerializer
from .views import QuotasViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('quote', QuotasViewSet)


app_name = "fin_api"

urlpatterns = [path('', include(router.urls))]
