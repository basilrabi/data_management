import os
import tempfile

from django.http import FileResponse
from django.template.loader import get_template

from custom.functions import export_csv
from location.models.source import Cluster

# pylint: disable=no-member

def export_cluster(request):
    rows = ([
        str(cluster.name),
        str(cluster.z),
        str(cluster.ore_class),
        str(cluster.mine_block),
        str(cluster.ni),
        str(cluster.fe),
        str(cluster.co),
        str(cluster.with_layout),
        str(cluster.excavated),
        str(cluster.geom.ewkt)
    ] for cluster in Cluster.objects.exclude(ni__lt=0.01))
    return export_csv(rows, 'location_cluster')

def export_cluster_str(request):
    context = {'clusters': Cluster.objects.all()}
    template = get_template('location/cluster.str')
    rendered_tpl = template.render(context)
    with tempfile.TemporaryDirectory() as tempdir:
        filename = os.path.join(tempdir, 'cluster.str')
        with open(filename, 'x', encoding='utf-8') as f:
            f.write(rendered_tpl)
        response = FileResponse(open(filename, 'rb'),
                                content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=cluster.str'
        return response
