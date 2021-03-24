from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as gettext


class UserCandidate(models.Model):
    is_candidate = models.BooleanField(
        default=False, verbose_name=gettext("This user is candidate")
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True,
        verbose_name=User._meta.verbose_name, related_name='candidate'
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
