from location.models.source import Cluster
# pylint: disable=no-member
for cluster in Cluster.objects.all():
    if cluster.geom:
        cluster.save()
        print(f'Cluster {cluster.name} snapped.', flush=True)
