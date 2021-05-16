from colorfield.fields import ColorField
from django.db import models
from django.utils.translation import gettext_lazy as gettext


class List(models.Model):
    name = models.CharField(
        verbose_name=gettext("Name"), max_length=128
    )

    color = ColorField(default='#aaa')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext("List")
        verbose_name_plural = gettext("Lists")

        ordering = ('name',)

        db_table = 'vc_lists'
