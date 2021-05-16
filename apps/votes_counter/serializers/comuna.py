from rest_framework import serializers
from .. import models


class Comuna(serializers.ModelSerializer):
    class Meta:
        model = models.Comuna
        fields = ('id', 'name',)
