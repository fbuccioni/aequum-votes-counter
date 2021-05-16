from collections import OrderedDict

from django.utils.text import slugify
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.votes_counter import models


@api_view(["GET"])
def view(request):
    output_json = OrderedDict()
    candidates = models.UserCandidate \
        .objects \
        .prefetch_related('user') \
        .order_by('user__first_name', 'user__last_name') \
        .filter(is_candidate=True)

    for candidate in candidates:
        full_name = f"{candidate.user.first_name} {candidate.user.last_name}"
        output_json[full_name] = OrderedDict(
            (
                ('id', candidate.pk),
                ('color', candidate.color),
                ('image', f"/static/images/candidates/{slugify(full_name)}.jpg")
            )
        )

    return Response(output_json)
