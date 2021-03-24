from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .polling_place_table import PollingPlaceTable


class Votes(models.Model):
    candidate = models.ForeignKey(
        User, on_delete=models.RESTRICT, null=True, blank=True,
        related_name="votes"
    )
    polling_place_table = models.ForeignKey(
        PollingPlaceTable, on_delete=models.RESTRICT,
        related_name="votes"
    )
    count = models.IntegerField(
        verbose_name=gettext("Votes count")
    )

    class Meta:
        verbose_name = gettext("Votes")
        verbose_name_plural = gettext("Votes")

        db_table = 'vc_polling_places_tables_votes'
