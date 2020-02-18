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
