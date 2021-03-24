import logging
import sys

from django.utils.translation import gettext_lazy as gettext
from django.apps import AppConfig
from django.core.management import call_command

logging.addLevelName(logging.INFO,  'info ')
logging.addLevelName(logging.WARN,  'warn ')
logging.addLevelName(logging.ERROR, 'error')
logging.addLevelName(logging.DEBUG, 'debug')


class Config(AppConfig):
    name: str = "apps.votes_counter"
    label: str = "votes_counter"
    verbose_name: str = gettext("Votes counter")

    @classmethod
    def ready(cls):
        if not sys.argv or not sys.argv[0].endswith("manage.py"):
            call_command('migrate')
