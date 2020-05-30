import os
import tempfile

from django.http import FileResponse
from django.template.loader import get_template

from custom.functions import export_csv
from location.models.source import Cluster, DrillHole

# pylint: disable=no-member

def export_cluster(request):
    """
    CSV view of Cluster intended for importation to database.
    """
    rows = ([
        str(cluster.name),
        str(cluster.z),
        str(cluster.distance_from_road or ''),
        str(cluster.road or ''),
        str(cluster.date_scheduled or ''),
        str(cluster.layout_date or ''),
        str(cluster.geom.ewkt)
    ] for cluster in Cluster.objects.exclude(ni__lt=0.01).order_by('count', 'mine_block', 'ore_class'))
    return export_csv(rows, 'location_cluster')

def export_cluster2(request):
    """
    CSV view of Cluster intended for user's perusal.
    """
    rows = ([
        str(cluster.name),
        str(cluster.z),
        str(cluster.ore_class),
        str(cluster.mine_block),
        str(cluster.ni),
        str(cluster.fe),
        str(cluster.co),
        str(cluster.date_scheduled or ''),
        str(cluster.layout_date or ''),
        str(round(cluster.geom.area * 3, 2))
    ] for cluster in Cluster.objects.exclude(excavated=True))
    return export_csv(rows, 'location_cluster')

def export_cluster_str(request):
    """
    A view of all Cluster exported in a string file. A string file (.str) is a
    file format fully compatible with Surpac.
    https://www.cse.unr.edu/~fredh/papers/working/vr-mining/string.html
    """
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

def export_drillhole(request):
    """
    CSV view of DrillHole intended for importation to database.
    """
    rows = ([
        str(dh.name),
        str(dh.date_drilled or ''),
        str(dh.local_block or ''),
        str(dh.local_easting or ''),
        str(dh.local_northing or ''),
        str(dh.local_z or ''),
        str(dh.x or ''),
        str(dh.y or ''),
        str(dh.z or ''),
        str(dh.z_present or '')
    ] for dh in DrillHole.objects.all().order_by('name'))
    return export_csv(rows, 'location_drillhole')
