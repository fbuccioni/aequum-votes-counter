from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import signals
from django.dispatch import receiver
from colorfield.fields import ColorField
from django.utils.translation import gettext_lazy as gettext

from .list import List


class UserCandidate(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True,
        verbose_name=User._meta.verbose_name, related_name='candidate'
    )

    is_candidate = models.BooleanField(
        default=False, verbose_name=gettext("This user is candidate")
    )

    list = models.ForeignKey(
        List, verbose_name=List._meta.verbose_name,
        on_delete=models.RESTRICT, null=True, blank=True
    )

    color = ColorField(default='#aaa')

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            return super().delete(*args, **kwargs)

    def __str__(self):
        return "%s %s" % (
            self.user.first_name, self.user.last_name
        )

    class Meta:
        verbose_name = gettext("Candidate user config")
        verbose_name_plural = gettext("Candidate users config")

        db_table = 'vc_user_candidates'


@receiver(signals.post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'candidate'):
        UserCandidate.objects.create(user=instance)

    if hasattr(instance, 'user_extra_conf'):
        instance.candidate.save()


@receiver(signals.post_save, sender=UserCandidate)
def candidate_vote_create_signal(sender, instance, created, **kwargs):
    from .polling_place_table import PollingPlaceTable
    from .votes import Votes

    if instance.is_candidate:
        for polling_place_table in PollingPlaceTable.objects.only("id").all():
            if (
                not Votes.objects
                .filter(
                    polling_place_table=polling_place_table,
                    candidate=instance
                ) \
                .count()
            ):
                Votes.objects.create(
                    polling_place_table=polling_place_table,
                    candidate=instance
                )
    else:
        Votes.objects.filter(candidate=instance).delete()


@receiver(signals.pre_delete, sender=UserCandidate)
def candidate_vote_delete_signal(sender, instance, using, **kwargs):
    from .votes import Votes

    if instance.is_candidate:
        Votes.objects.filter(candidate=instance).delete()
