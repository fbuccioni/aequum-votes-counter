from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from ... import serializers, models


class PollingPlaceTable(ListModelMixin, GenericViewSet):
    serializer_class = serializers.PollingPlaceTable
    queryset = models.PollingPlaceTable.objects

    def get_queryset(self):
        return super().get_queryset().filter(
            polling_place_id=self.kwargs['polling_place_id'],
            polling_place__comuna_id=self.kwargs['comuna_id']
        )