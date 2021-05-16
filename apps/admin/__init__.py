"""
django-votes_counter.rst admin file example.
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as gettext
from . import votes_counter


class AdminSite(admin.sites.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = gettext('Votes counter administration')

    # Text to put in each page's <h1> (and above login form).
    site_header = gettext('Votes counter administration')

    # Text to put at the top of the admin index page.
    index_title = gettext('Administration')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry.update(admin.site._registry)


site = AdminSite()

site.unregister(User)
site.register(User, votes_counter.CustomUserAdmin)

for admin_module in (votes_counter,):
    for item in dir(admin_module):
        model_admin = getattr(admin_module, item)

        if hasattr(model_admin, 'ignore_auto'):
            continue

        try:
            is_class = issubclass(model_admin, object)
        except TypeError:
            is_class = False

        if is_class and issubclass(model_admin, admin.ModelAdmin):
            site.register(getattr(admin_module.models, item), model_admin)

