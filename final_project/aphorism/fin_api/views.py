from django.db.models import Q
from django.http import HttpResponseRedirect
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import QuoteSerializer, MessageSerializer
from rest_framework import viewsets, permissions
from scrap.models import Quotas, Authors, Messege


class QuotasViewSet(viewsets.ModelViewSet):
    queryset = Quotas.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.first_name:
            auth = f'{self.request.user.first_name} {self.request.user.last_name}'
            a, _ = Authors.objects.get_or_create(author=auth)
            serializer.save(author=a)
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        q = Quotas.objects.filter(user=self.request.user).all()
        if q and len(q) < 2 and q[0].author:
            Authors.objects.filter(author=q[0].author).delete()
        instance.delete()

    def get_queryset(self):
        if self.request.method in ['PUT', 'DELETE']:
            queryset = self.queryset.filter(user=self.request.user)
            return queryset
        return self.queryset

    @action(detail=True, methods=['get'])
    def add_remove_fav(self, request, pk=None):
        quote = get_object_or_404(Quotas, id=pk)

        if quote.fav.filter(id=request.user.id).exists():
            quote.fav.remove(request.user)
            return Response(data={'fav': False})
        else:
            quote.fav.add(request.user)

        return Response(data={'fav': True})


'''Messages'''


class MessageViewSet(viewsets.ModelViewSet):

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    #
    # def perform_destroy(self, instance):
    #     q = Quotas.objects.filter(user=self.request.user).all()
    #     if q and len(q) < 2 and q[0].author:
    #         Authors.objects.filter(author=q[0].author).delete()
    #     instance.delete()
    #
    def get_queryset(self):
        queryset = Messege.objects.filter(
            Q(reciever=self.request.user) | Q(sender=self.request.user)).order_by('-date')
        return queryset
