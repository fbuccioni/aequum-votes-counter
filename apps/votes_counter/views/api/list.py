from collections import OrderedDict

from django.utils.text import slugify
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.votes_counter import models


@api_view(["GET"])
def view(request):
    output_json = OrderedDict()
    lists = models.List \
        .objects \
        .all()

    for lst in lists:
        full_name = f"{lst.name}"
        output_json[full_name] = OrderedDict(
            (
                ('id', lst.pk),
                ('color', lst.color),
                ('image', f"/static/images/lists/{slugify(full_name)}.jpg")
            )
        )

    return Response(output_json)
