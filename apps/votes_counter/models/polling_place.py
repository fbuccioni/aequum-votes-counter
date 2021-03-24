from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .comuna import Comuna


class PollingPlace(models.Model):
    name = models.CharField(
        verbose_name=gettext("Polling place"), max_length=255
    )

    comuna = models.ForeignKey(
        Comuna, on_delete=models.PROTECT, related_name="polling_places"
    )

    class Meta:
        verbose_name = gettext("Polling place")
        verbose_name_plural = gettext("Polling places")

        db_table = 'vc_polling_places'
