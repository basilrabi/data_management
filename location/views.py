import ezdxf

from django.http import FileResponse
from django.template.loader import get_template
from os.path import join
from subprocess import PIPE, run
from tempfile import TemporaryDirectory

from custom.functions import export_sql
from location.models.source import Cluster

# pylint: disable=no-member

def export_cluster(request):
    """
    CSV view of Cluster intended for user's perusal.
    """
    return export_sql('export_clusters', 'clusters')

def export_cluster_dxf_for_survey(request):
    """
    Export clusters relevant to survey in dxf format.
    """
    scheduled_dates = Cluster.objects \
        .filter(excavated=False, date_scheduled__isnull=False, geom__isnull=False) \
        .order_by('date_scheduled') \
        .values('date_scheduled').distinct()
    with TemporaryDirectory() as tempdir:
        if scheduled_dates.count() > 0:
            run(f'cd "{tempdir}" && mkdir dxf', shell=True, stdout=PIPE, stderr=PIPE)
            for item in scheduled_dates:
                date = f"{item['date_scheduled']}"
                clusters = Cluster.objects.filter(date_scheduled=date)
                doc = ezdxf.new('R2013')
                doc.appids.new('TrimbleName')
                for cluster in clusters:
                    msp = doc.modelspace()
                    doc.layers.new(name=f'{cluster.name}')
                    geom = cluster.geom.tuple
                    for multi_polygon in geom:
                        for polygon in multi_polygon:
                            entity = msp.add_lwpolyline(
                                list(polygon),
                                dxfattribs={
                                    'layer': f'{cluster.name}',
                                    'linetype': 'CONTINUOUS',
                                    'color': cluster.getACI(),
                                    'elevation': cluster.z - 3
                                }
                            )
                            entity.set_xdata('TrimbleName', [
                                (1001, 'TrimbleName'),
                                (1000, f'{cluster.name}'),
                            ])
                doc.saveas(join(tempdir, 'dxf', f'{date}.dxf'))
            command = f'cd "{tempdir}"/dxf && zip ../clusters.zip *'
            run(command, shell=True, stdout=PIPE, stderr=PIPE)
            filename = join(tempdir, 'clusters.zip')
            return FileResponse(open(filename, 'rb'), content_type='application/zip')
        else:
            command = f'cd "{tempdir}" && ' + \
                'echo "There is no un-excavated scheduled block." > output.txt'
            run(command, shell=True, stdout=PIPE, stderr=PIPE)
            filename = join(tempdir, 'output.txt')
            return FileResponse(open(filename, 'rb'), content_type='text/plain')


def export_cluster_str(request):
    """
    A view of all Cluster exported in a string file. A string file (.str) is a
    file format fully compatible with Surpac.
    https://www.cse.unr.edu/~fredh/papers/working/vr-mining/string.html
    """
    context = {'clusters': Cluster.objects.all().exclude(geom=None)}
    template = get_template('location/cluster.str')
    rendered_tpl = template.render(context)
    with TemporaryDirectory() as tempdir:
        filename = join(tempdir, 'cluster.str')
        with open(filename, 'x', encoding='utf-8') as f:
            f.write(rendered_tpl)
        response = FileResponse(open(filename, 'rb'),
                                content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=cluster.str'
        return response

def export_cluster_str_for_survey(request):
    """
    Export clusters relevant to survey.
    """
    context = {'clusters': Cluster.objects.all().filter(latest_layout_date=None).exclude(date_scheduled=None)}
    template = get_template('location/cluster.str')
    rendered_tpl = template.render(context)
    with TemporaryDirectory() as tempdir:
        filename = join(tempdir, 'cluster.str')
        with open(filename, 'x', encoding='utf-8') as f:
            f.write(rendered_tpl)
        response = FileResponse(open(filename, 'rb'),
                                content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=cluster.str'
        return response
