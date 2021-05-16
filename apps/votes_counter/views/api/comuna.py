from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from ... import serializers, models


class Comuna(ListModelMixin, GenericViewSet):
    serializer_class = serializers.Comuna
    queryset = models.Comuna.objects
