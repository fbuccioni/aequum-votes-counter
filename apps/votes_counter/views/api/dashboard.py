from collections import OrderedDict

from django.db import connection
from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response

import apps.votes_counter.views.api.candidate
from ... import models


@api_view(["GET"])
def votes(request):
    output_json = OrderedDict()
    fetch_size = 20
    with connection.cursor() as cur:
        cur.execute("""
            SELECT      c.name as comuna,
                        p.name as polling_place,
                        t.name as `table`, 
                        IF(candidate_id IS NULL, 'Total', CONCAT(u.first_name, ' ', u.last_name)) as name,
                        l.name as list,
                        v.count as votes
            FROM        vc_polling_places_tables_votes v
            INNER JOIN  vc_polling_places_tables t ON v.polling_place_table_id = t.id
            INNER JOIN  vc_polling_places p ON t.polling_place_id = p.id
            INNER JOIN  vc_comunas c ON p.comuna_id = c.id
            LEFT JOIN   vc_user_candidates uc ON v.candidate_id = uc.user_id
            LEFT JOIN   auth_user u ON v.candidate_id = u.id
            LEFT JOIN   vc_lists l ON uc.list_id = l.id
            ORDER BY    c.name, p.name, t.name, name
        """)

        while True:
            rows = cur.fetchmany(fetch_size)
            if not rows:
                break

            for row in rows:
                comuna, polling_place, table, name, lst, votes = row
                if comuna not in output_json:
                    output_json[comuna] = OrderedDict()

                if polling_place not in output_json[comuna]:
                    output_json[comuna][polling_place] = OrderedDict()

                if table not in output_json[comuna][polling_place]:
                    output_json[comuna][polling_place][table] = OrderedDict((
                        ('candidates', OrderedDict()),
                        ('lists', OrderedDict()),
                    ))

                if name not in output_json[comuna][polling_place][table]['candidates']:
                    output_json[comuna][polling_place][table]['candidates'][name] = 0

                if name not in output_json[comuna][polling_place][table]['lists']:
                    output_json[comuna][polling_place][table]['lists'][lst] = 0

                output_json[comuna][polling_place][table]['candidates'][name] += votes
                output_json[comuna][polling_place][table]['lists'][lst] += votes

    return Response(output_json)
