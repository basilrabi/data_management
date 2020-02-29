from location.models.source import Cluster
# pylint: disable=no-member
for cluster in Cluster.objects.all():
    if cluster.geom:
        if cluster.distance_from_road is None:
            cluster.distance_from_road = 0
            cluster.save()
            cluster.distance_from_road = None
            cluster.save()
        else:
            distance = cluster.distance_from_road
            cluster.distance_from_road = None
            cluster.save()
            cluster.distance_from_road = distance
            cluster.save()
        print(f'Cluster {cluster.name} snapped.', flush=True)
