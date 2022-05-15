from scrap.models import Quotas
from rest_framework.serializers import ModelSerializer

class QuoteSerializer(ModelSerializer):
    class Meta:
        model = Quotas
        fields = ['id', 'quota', 'author', 'tag']
        read_only = ['author','user']

        #f984d34d9dd03c464c450c7c222b447646dfb840
        #ecc4d0a210f001c89991eba470c65e57eda248be