from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .polling_place import PollingPlace


class PollingPlaceTable(models.Model):
    name = models.CharField(
        verbose_name=gettext("Polling place table"), max_length=64
    )

    polling_plpace = models.ForeignKey(
        PollingPlace, on_delete=models.PROTECT, related_name="tables"
    )

    class Meta:
        verbose_name = gettext("Polling place table")
        verbose_name_plural = gettext("Polling places tables")

        db_table = 'vc_polling_placesgettextables'
