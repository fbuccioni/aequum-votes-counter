from django.db.models import QuerySet, F
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from ... import serializers, models
import operator


class Votes(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = serializers.Votes
    queryset = models.Votes.objects

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(
            polling_place_table_id=self.kwargs['polling_place_table_id'],
        )

    def create(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            raise ValidationError("Input data must be an array")

        for op in request.data:
            op_op = operator.add if op['op'] == "add" else operator.sub
            self.get_queryset()\
                .filter(candidate_id=op['candidate'])\
                .update(count=op_op(F('count'), op['cant']))

        return self.list(self, request, *args, **kwargs)