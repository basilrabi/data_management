from django.shortcuts import render

from custom.functions import export_csv
from inventory.models.insitu import Block

# pylint: disable=no-member

def index(request):
    return render(request, 'inventory/index.html', {})

def export_clustered_block(request):
    """
    Names of the block with foreign key relation to `location_cluster`. This is
    intended for importation of the foreign key relation to the database.
    """
    rows = ([
        str(block.name)
    ] for block in Block.objects.exclude(cluster__isnull=True).order_by('name'))
    return export_csv(rows, 'inventory_clustered_block')

def export_clustered_block2(request):
    """
    CSV view of clustered Block intended for user's perusal.
    """
    rows = ([
        str(block.cluster_name),
        str(block.name),
        str(block.z),
        str(block.ni),
        str(block.fe),
        str(block.co),
        str(round(block.volume, 2))
    ] for block in Block.objects.raw(
        '''
        SELECT
            block.id id,
            cluster.name cluster_name,
            block.name "name",
            block.z z,
            block.ni ni,
            block.fe fe,
            block.co co,
            ST_Area(
                ST_Intersection(ST_Expand(block.geom, 5), cluster.geom)
            ) * 3 volume
        FROM location_cluster cluster INNER JOIN inventory_block block
        ON cluster.id = block.cluster_id
        WHERE cluster.excavated = false
        ORDER BY "name";
        '''
    ))

    return export_csv(rows, 'clustered_block')
