from django.db import models
from django.utils.translation import gettext_lazy as gettext


class Comuna(models.Model):
    name = models.CharField(
        verbose_name=gettext("Name"), max_length=128
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext("Comuna")
        verbose_name_plural = gettext("Comunas")
        
        ordering = ('name',)

        db_table = 'vc_comunas'
