from location.models.source import Cluster
# pylint: disable=no-member
for cluster in Cluster.objects.all():
    if cluster.geom:
        old_name = cluster.name
        block = cluster.block_set.first()
        block.cluster = None
        block.save()
        block.cluster = cluster
        block.save()
        cluster.refresh_from_db()
        print(f'Cluster {old_name} snapped and converted to {cluster.name}.', flush=True)
