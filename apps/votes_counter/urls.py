"""votes_counter URL Configuration

The `urls` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path, path, include
from django.utils.translation import gettext_lazy as gettext
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views
from .rest import routers

schema_view = get_schema_view(
   openapi.Info(
      title=gettext("Aequum votes counter API"),
      default_version='1.0.0',
      description=gettext("Web application"),
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="felipe.buccioni@gmail.com"),
      license=openapi.License(name="Commercial"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


api_path = path(
    'api/', include(
        # Main viewsets
        routers.DefaultRouter([
            #(r'thing', views.api.object.ThingViewSet, "api.thing"),
        ]).urls + [
        # Additional views
            #path(
            #    'thing/<id>/other-action/', views.api.thing.other_action, name="api.user.places.list"
            #),
        ]
    )
)


# Documentation in `/api/specs`
api_path.url_patterns.append(
    path('specs/', include([
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='api.schema.file'),
        path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='api.schema.swaggerui'),
        path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api.schema.redoc'),
    ]))
)

urlpatterns = [
    path('', views.skeretonu),
    api_path,
]
