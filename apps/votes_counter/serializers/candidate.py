from rest_framework import serializers
from .. import models


class Candidate(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    @staticmethod
    def get_candidate_obj(obj):
        return obj

    @classmethod
    def get_name(cls, obj):
        obj = cls.get_candidate_obj(obj)

        if not obj:
            return None
        else:
            return '{} {}'.format(
                obj.user.first_name,
                obj.user.last_name
            )

    class Meta:
        model = models.UserCandidate
        fields = ('name',)
