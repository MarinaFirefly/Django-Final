from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated

from API.serializers import FilmSerializer, PurchaseSerializer
from cinema.models import Film, Purchase


class FilmViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FilmSerializer
    queryset = Film.objects.all()


class PurchaseViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return PurchaseSerializer
        return super().get_serializer_class()
