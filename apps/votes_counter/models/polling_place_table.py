from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as gettext

from .polling_place import PollingPlace


class PollingPlaceTable(models.Model):
    name = models.CharField(
        verbose_name=gettext("Polling place table"), max_length=64
    )

    polling_place = models.ForeignKey(
        PollingPlace, on_delete=models.PROTECT, related_name="tables"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = gettext("Polling place table")
        verbose_name_plural = gettext("Polling places tables")

        db_table = 'vc_polling_places_tables'
        ordering = ('name',)


@receiver(signals.post_save, sender=PollingPlaceTable)
def polling_place_table_total_votes_create(sender, instance, created, **kwargs):
    from .votes import Votes

    if created:
        Votes.objects.create(
            candidate=None,
            polling_place_table=instance
        )


@receiver(signals.pre_delete, sender=PollingPlaceTable)
def polling_place_table_total_votes_delete(sender, instance, using, **kwargs):
    from .votes import Votes

    Votes.objects.filter(polling_place_table=instance).delete()
