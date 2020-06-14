# pylint: disable=import-error
# pylint: disable=no-member
from location.models.source import Cluster
for cluster in Cluster.objects.raw(
    '''
    SELECT
        id,
        name,
        substring(name, '^[A-Z](\\d+)-\\d+-\\d+$')::int count,
        substring(name, '^[A-Z]\\d+-\\d+-(\\d+)$') mine_block,
        substring(name, '^([A-Z])\\d+-\\d+-\\d+$') ore_class
    FROM location_cluster
    WHERE geom IS NOT NULL
    ORDER BY count, mine_block, ore_class;
    '''
):
    old_name = cluster.name
    block = cluster.block_set.first()
    block.cluster = None
    block.save()
    block.cluster = cluster
    block.save()
    cluster.refresh_from_db()
    new_name = cluster.name
    if old_name == new_name:
        print(f'{old_name} snapped.', flush=True)
    else:
        print(f'{old_name} -> {new_name}.', flush=True)
