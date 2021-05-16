from rest_framework import serializers
from .. import models


class PollingPlace(serializers.ModelSerializer):
    class Meta:
        model = models.PollingPlace
        fields = ('id', 'name')
