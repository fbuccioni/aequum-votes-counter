from collections import OrderedDict

from rest_framework.decorators import api_view
from rest_framework.response import Response

import apps.votes_counter.views.api.candidate
from ... import models


@api_view(["GET"])
def votes(request):
    output_json = OrderedDict()
    comunas = models.Comuna.objects.all()

    for comuna in comunas:
        output_json[comuna.name] = \
        output_json_comuna = OrderedDict()
        for polling_place in comuna.polling_places.all():
            output_json_comuna[polling_place.name] = \
            output_json_comuna_polling_place = OrderedDict()
            for table in polling_place.tables.all():
                output_json_comuna_polling_place[table.name] = \
                output_json_comuna_polling_place_table = OrderedDict((
                    ('candidates', OrderedDict()),
                    ('lists', OrderedDict()),
                ))

                table_votes = table.votes.all()
                for votes in table_votes:
                    if votes.candidate:
                        name = f"{votes.candidate.user.first_name} {votes.candidate.user.last_name}"
                    else:
                        name = "Total"

                    output_json_comuna_polling_place_table['candidates'][name] = votes.count

                for votes in table_votes:
                    if votes.candidate:
                        name = f"{votes.candidate.list.name}"
                    else:
                        name = "Total"

                    if name not in output_json_comuna_polling_place_table['lists']:
                        output_json_comuna_polling_place_table['lists'][name] = 0

                    output_json_comuna_polling_place_table['lists'][name] += votes.count

    return Response(output_json)
