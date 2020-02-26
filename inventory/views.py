from django.shortcuts import render

from custom.functions import export_csv
from inventory.models.insitu import Block

# pylint: disable=no-member

def index(request):
    return render(request, 'inventory/index.html', {})

def export_clustered_block(request):
    rows = ([
        str(block.name)
    ] for block in Block.objects.exclude(cluster__isnull=True))
    return export_csv(rows, 'inventory_clustered_block')
