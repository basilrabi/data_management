import os
import pandas as pd
import plotly.graph_objects as go
import tempfile

from django.db import connection
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from plotly.offline import plot
from subprocess import PIPE, run

from custom.functions import export_sql
from shipment.models.dso import LayDaysStatement

# pylint: disable=no-member

def index(request):
    loading_per_shipment = ''
    with connection.cursor() as cursor:
        cursor.execute("""
        WITH cte_a AS (
            SELECT
                EXTRACT(EPOCH FROM ja.interval_from) - EXTRACT(EPOCH FROM a.interval_from) AS time_elapsed,
                CASE
                    WHEN a.interval_class = 'continuous loading' THEN 'Loading'
                    WHEN a.interval_class IN ('heavy swell', 'rain', 'rain and heavy swell') THEN 'Natural Delay'
                    WHEN a.interval_class = 'vessel arrived behind of schedule' THEN 'Arrival Delay'
                    ELSE 'Idle'
                END interval_class,
                d.name shipment,
                c.completed_loading
            FROM shipment_laydaysdetail a
                LEFT JOIN LATERAL (
                    SELECT b.interval_from
                    FROM shipment_laydaysdetail b
                    WHERE b.laydays_id = a.laydays_id
                        AND b.interval_from > a.interval_from
                    ORDER BY b.interval_from ASC LIMIT 1
                ) ja ON true
                LEFT JOIN shipment_laydaysstatement c
                    ON c.id = a.laydays_id
                LEFT JOIN shipment_shipment d
                    ON d.id = c.shipment_id
            WHERE ja.interval_from IS NOT NULL
                AND c.completed_loading IS NOT NULL
        ),
        cte_b AS (
            SELECT
                shipment,
                completed_loading,
                interval_class,
                sum(time_elapsed) / (60 * 60 * 24) AS duration
            FROM cte_a
            GROUP BY shipment, completed_loading, interval_class
        ),
        cte_c AS (
            SELECT
                shipment,
                completed_loading,
                interval_class,
                duration,
                sum(duration) OVER (PARTITION BY shipment) total_duration
            FROM cte_b
        )
        SELECT
            shipment,
            completed_loading,
            interval_class,
            duration,
            'Total: ' || round(total_duration::numeric, 2)
        FROM cte_c
        ORDER BY completed_loading
        """)
        df = pd.DataFrame.from_records(cursor.fetchall())
        box_data = []
        for interval_class in df[2].unique():
            df_filtered = df[df[2] == interval_class]
            box_data.append(
                go.Bar(
                    name=interval_class,
                    x=df_filtered[0],
                    y=df_filtered[3],
                    text=df_filtered[4]
                )
            )
        fig_loading_per_shipment = go.Figure(data=box_data)
        fig_loading_per_shipment.update_layout(
            barmode='stack',
            legend_title_text='Interval',
            title='Ship Loading Duration',
            xaxis_title='Shipment',
            yaxis_title='Days Elapsed'
        )
        loading_per_shipment = plot(
            fig_loading_per_shipment,
            output_type='div',
            include_plotlyjs=False
        )
    return render(request, 'shipment/index.html', {
        'loading_per_shipment': loading_per_shipment
    })

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
