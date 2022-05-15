from .serializers import QuoteSerializer
from rest_framework import viewsets, permissions
from scrap.models import Quotas, Authors




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
        if q and len(q) < 2:
            Authors.objects.filter(author=q[0].author).delete()
        instance.delete()


    def get_queryset(self):
        if self.request.method in ['PUT', 'DELETE']:
            queryset = self.queryset.filter(user=self.request.user)
            return queryset
        return self.queryset




