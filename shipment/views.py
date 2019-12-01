import os
import tempfile

from django.http import FileResponse
from django.template.loader import get_template
from subprocess import PIPE, run

from shipment.models.dso import LayDaysStatement

def lay_days_statement_pdf(request, name):
    # pylint: disable=E1101
    statement = LayDaysStatement.objects.get(shipment__name=name)
    details = statement.laydaysdetail_set.all()
    context = {
        'statement': statement,
        'details': details
    }
    template = get_template('shipment/lay_time_statement.tex')
    rendered_tpl = template.render(context)
    with tempfile.TemporaryDirectory() as tempdir:
        filename = os.path.join(tempdir, 'texput.tex')
        with open(filename, 'x', encoding='utf-8') as f:
            f.write(rendered_tpl)
        latex_command = f'cd "{tempdir}" && pdflatex --shell-escape ' + \
            f'-interaction=batchmode {os.path.basename(filename)}'
        run(latex_command, shell=True, stdout=PIPE, stderr=PIPE)
        run(latex_command, shell=True, stdout=PIPE, stderr=PIPE)
        return FileResponse(open(os.path.join(tempdir, 'texput.pdf'), 'rb'),
                            content_type='application/pdf')
