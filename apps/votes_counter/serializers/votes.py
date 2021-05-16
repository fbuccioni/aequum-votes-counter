from rest_framework import serializers
from .. import models

from .candidate import Candidate


class Votes(serializers.ModelSerializer):
    name = Candidate._declared_fields['name']
    get_name = classmethod(Candidate.get_name.__func__)

    @staticmethod
    def get_candidate_obj(obj):
        return obj.candidate

    class Meta:
        model = models.Votes
        fields = ('id', 'name', 'count')
