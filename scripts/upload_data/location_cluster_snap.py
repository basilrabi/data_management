# pylint: disable=import-error
# pylint: disable=no-member
from location.models.source import Cluster

# Snap only one cluster to create a blank cluster.
cluster = Cluster.objects.first()
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
