from django.db import models
from django.utils.translation import gettext_lazy as gettext


class Comuna(models.Model):
    name = models.CharField(
        verbose_name=gettext("Name"), max_length=128
    )

    class Meta:
        verbose_name = gettext("Comuna")
        verbose_name_plural = gettext("Comunas")

        db_table = 'vc_comunas'
