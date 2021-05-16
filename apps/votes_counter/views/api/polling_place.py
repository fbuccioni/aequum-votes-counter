from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from ... import serializers, models


class PollingPlace(ListModelMixin, GenericViewSet):
    serializer_class = serializers.PollingPlace
    queryset = models.PollingPlace.objects

    def get_queryset(self):
        return super().get_queryset().filter(comuna=self.kwargs['comuna_id'])