import os
import tempfile

from django.http import FileResponse, HttpResponse
from django.template.loader import get_template
from subprocess import PIPE, run

from custom.functions import export_sql
from shipment.models.dso import LayDaysStatement

# pylint: disable=no-member

def data_export_laydays(request):
    """
    CSV view of LayDaysDetail intended for user's perusal.
    """
    return export_sql('export_laydays', 'laydays_detail')

def data_export_lct_trips(request):
    """
    CSV view of TripDetail intended for user's perusal.
    """
    return export_sql('export_lcttrips', 'lct_trips')

def lay_days_statement_csv(request, name):
    statement = LayDaysStatement.objects.get(shipment__name=name)
    statement._compute()
    details = statement.laydaysdetailcomputed_set.all()
    context = {'details': details}
    template = get_template('shipment/lay_time_details.csv')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{statement.shipment.name}.csv"'
    response.write(template.render(context))
    return response

def lay_days_statement_pdf(request, name):
    statement = LayDaysStatement.objects.get(shipment__name=name)
    statement._compute()
    details = statement.laydaysdetailcomputed_set.all()
    context = {
        'statement': statement,
        'details': details
    }
    template = get_template('shipment/lay_time_statement.tex')
    rendered_tpl = template.render(context)
    with tempfile.TemporaryDirectory() as tempdir:
        filename = os.path.join(tempdir, f'{statement.shipment.name}.tex')
        with open(filename, 'x', encoding='utf-8') as f:
            f.write(rendered_tpl)
        latex_command = f'cd "{tempdir}" && pdflatex --shell-escape ' + \
            f'-interaction=batchmode {os.path.basename(filename)}'
        run(latex_command, shell=True, stdout=PIPE, stderr=PIPE)
        run(latex_command, shell=True, stdout=PIPE, stderr=PIPE)
        return FileResponse(
            open(os.path.join(tempdir, f'{statement.shipment.name}.pdf'), 'rb'),
            content_type='application/pdf'
        )
