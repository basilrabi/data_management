import os
import tempfile

from django.http import FileResponse
from django.template.loader import get_template
from subprocess import PIPE, run

from sampling.models.sample import ShipmentLoadingAssay

# pylint: disable=no-member

def assay_certificate(request, name):
    assay = ShipmentLoadingAssay.objects.get(shipment__name=name)
    lots = assay.shipmentloadinglotassay_set.all()
    context = {
        'assay': assay,
        'lots': lots
    }
    template = get_template('sampling/assay_certificate.tex')
    rendered_tpl = template.render(context)
    with tempfile.TemporaryDirectory() as tempdir:
        filename = os.path.join(tempdir, f'{assay.__str__()}.tex')
        with open(filename, 'x', encoding='utf-8') as f:
            f.write(rendered_tpl)
        latex_command = f'cd "{tempdir}" && pdflatex --shell-escape ' + \
            f'-interaction=batchmode {os.path.basename(filename)}'
        run(latex_command, shell=True, stdout=PIPE, stderr=PIPE)
        run(latex_command, shell=True, stdout=PIPE, stderr=PIPE)
        return FileResponse(
            open(os.path.join(tempdir, f'{assay.__str__()}.pdf'), 'rb'),
            content_type='application/pdf'
        )
