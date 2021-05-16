from rest_framework import serializers
from .. import models


class PollingPlaceTable(serializers.ModelSerializer):
    class Meta:
        model = models.PollingPlaceTable
        fields = ('id', 'name')
