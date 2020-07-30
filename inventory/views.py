from django.shortcuts import render

from custom.functions import export_csv, export_sql
from inventory.models.insitu import Block

# pylint: disable=no-member

def index(request):
    return render(request, 'inventory/index.html', {})

def export_clustered_block(request):
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
        str(block.volume)
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
            round(
                (
                    ST_Area(
                        ST_Intersection(
                            ST_Expand(block.geom, 5),
                            cluster.geom
                        )
                    ) * 3
                )::numeric,
                2
            ) volume
        FROM inventory_block block LEFT JOIN location_cluster cluster
        ON cluster.id = block.cluster_id
        WHERE block.cluster_id IS NOT NULL
        ORDER BY cluster.ore_class,
                 cluster.count,
                 cluster_name,
                 "name";
        '''
    ))

    return export_csv(rows, 'clustered_block')

def scheduled_block(request):
    """
    CSV view for number of scheduled blocks in MineSched.
    """
    return export_sql('view_plan_vs_cluster', 'plan_vs_cluster')
