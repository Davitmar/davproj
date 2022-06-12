from scrap.models import Quotas, Messege
from rest_framework.serializers import ModelSerializer


class QuoteSerializer(ModelSerializer):
    class Meta:
        model = Quotas
        fields = ['id', 'quota', 'author', 'tag']
        read_only = ['author', 'user']


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Messege
        fields = ['id', 'messege', 'nkar', 'sender', 'reciever', 'date']
        read_only = ['sender', 'date']
