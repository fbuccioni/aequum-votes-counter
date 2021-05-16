from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .polling_place_table import PollingPlaceTable
from .candidate import UserCandidate


class Votes(models.Model):
    candidate = models.ForeignKey(
        UserCandidate, on_delete=models.RESTRICT, null=True, blank=True,
        related_name="votes"
    )
    polling_place_table = models.ForeignKey(
        PollingPlaceTable, on_delete=models.RESTRICT,
        related_name="votes"
    )
    count = models.IntegerField(
        verbose_name=gettext("Votes count"), default=0
    )

    def __str__(self):
        if self.candidate:
            return gettext("Votes of %s in %s") % (
                str(self.candidate),
                self.polling_place_table.name
            )
        else:
            return gettext("Total votes in %s") % self.polling_place_table.name

    class Meta:
        verbose_name = gettext("Votes")
        verbose_name_plural = gettext("Votes")
        unique_together = (
            ('polling_place_table', 'candidate')
        )

        db_table = 'vc_polling_places_tables_votes'
