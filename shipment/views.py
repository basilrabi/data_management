import os
import tempfile

from django.http import FileResponse
from django.template.loader import get_template
from subprocess import PIPE, run

from custom.functions import export_csv, export_sql, print_localzone
from shipment.models.dso import LayDaysStatement, Shipment, Vessel
from shipment.models.lct import LCT, LCTContract, Trip

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

def export_laydaysstatement(request):
    """
    CSV view of LayDaysStatement intended for importation to database.
    """
    rows = ([
        str(statement.shipment.name),
        str(statement.vessel_voyage),
        str(print_localzone(statement.arrival_pilot) or ''),
        str(print_localzone(statement.arrival_tmc) or ''),
        str(print_localzone(statement.nor_tender) or ''),
        str(print_localzone(statement.nor_accepted) or ''),
        str(statement.cargo_description),
        str(statement.tonnage or ''),
        str(statement.loading_terms),
        str(statement.demurrage_rate),
        str(statement.despatch_rate),
        str(statement.can_test),
        str(statement.pre_loading_can_test),
        str(statement.report_date or ''),
        str(statement.revised)
    ] for statement in LayDaysStatement.objects.all().order_by('completed_loading', 'shipment__name'))
    return export_csv(rows, 'shipment_laydaysstatement')

def export_lct(request):
    """
    CSV view of LCT intended for importation to database.
    """
    rows = ([
        str(lct.name),
        str(lct.capacity)
    ] for lct in LCT.objects.all().order_by('name'))
    return export_csv(rows, 'shipment_lct')

def export_lctcontract(request):
    """
    CSV view of LCTContract intended for importation to database.
    """
    rows = ([
        str(contract.lct.name),
        str(contract.start),
        str(contract.end or '')
    ] for contract in LCTContract.objects.all().order_by('lct__name', 'start'))
    return export_csv(rows, 'shipment_lctcontract')

def export_shipment(request):
    """
    CSV view of Shipment intended for importation to database.
    """
    rows = ([
        str(shipment.vessel.name),
        str(shipment.name),
        str(shipment.dump_truck_trips),
        str(shipment.tonnage)
    ] for shipment in Shipment.objects.all().order_by('laydaysstatement__completed_loading', 'name'))
    return export_csv(rows, 'shipment_shipment')

def export_vessel(request):
    """
    CSV view of Vessel intended for importation to database.
    """
    rows = ([
        str(vessel.name)
    ] for vessel in Vessel.objects.all().order_by('name'))
    return export_csv(rows, 'shipment_vessel')

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
        filename = os.path.join(tempdir, f'{statement.__str__()}.tex')
        with open(filename, 'x', encoding='utf-8') as f:
            f.write(rendered_tpl)
        latex_command = f'cd "{tempdir}" && pdflatex --shell-escape ' + \
            f'-interaction=batchmode {os.path.basename(filename)}'
        run(latex_command, shell=True, stdout=PIPE, stderr=PIPE)
        run(latex_command, shell=True, stdout=PIPE, stderr=PIPE)
        return FileResponse(
            open(os.path.join(tempdir, f'{statement.__str__()}.pdf'), 'rb'),
            content_type='application/pdf'
        )
