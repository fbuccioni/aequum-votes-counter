"""
URL Configuration for proeject
"""

from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

from apps import admin
import apps.votes_counter.urls

urlpatterns = [
    path('_/jet/', include('jet.urls', 'jet')),
    path('js/i18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('admin/', admin.site.urls),
    path('', include(apps.votes_counter.urls))
]
