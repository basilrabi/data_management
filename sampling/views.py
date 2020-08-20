import os
import pandas as pd
import plotly.graph_objects as go
import tempfile

from django.db.models import F
from django.db.models.functions import ExtractYear
from django.http import FileResponse
from django.shortcuts import render
from django.template.loader import get_template
from plotly.offline import plot
from subprocess import PIPE, run

from sampling.models.sample import ShipmentLoadingAssay

# pylint: disable=no-member

def index(request):
    df = pd.DataFrame.from_records(
        ShipmentLoadingAssay.objects.all() \
            .annotate(
                laboratory=F('shipment__shipmentdischargeassay__laboratory__name'),
                ni_diff=F('ni') - F('shipment__shipmentdischargeassay__ni'),
                fe_diff=F('fe') - F('shipment__shipmentdischargeassay__fe'),
                loading_completion=F('shipment__laydaysstatement__completed_loading'),
                shipment_name=F('shipment__name'),
                year=ExtractYear(F('shipment__laydaysstatement__completed_loading'))
            ) \
            .exclude(ni_diff__isnull=True) \
            .exclude(loading_completion__isnull=True) \
            .values_list(
                'loading_completion',
                'ni_diff',
                'fe_diff',
                'laboratory',
                'shipment_name',
                'year'
            )
    )
    print(df[5].unique())

    fig_fe_diff_per_shipment = go.Figure()
    fig_fe_diff_per_year = go.Figure()
    fig_ni_diff_per_shipment = go.Figure()
    fig_ni_diff_per_year = go.Figure()
    for lab in df[3].unique():
        df_filtered = df[df[3] == lab]
        fig_fe_diff_per_shipment.add_trace(
            go.Scatter(
                x=df_filtered[0],
                y=df_filtered[2],
                name=lab,
                mode='lines+markers',
                text=df_filtered[4]
            )
        )
        fig_fe_diff_per_year.add_trace(
            go.Box(
                x=df_filtered[5],
                y=df_filtered[2],
                name=lab,
                boxmean=True
            )
        )
        fig_ni_diff_per_shipment.add_trace(
            go.Scatter(
                x=df_filtered[0],
                y=df_filtered[1],
                name=lab,
                mode='lines+markers',
                text=df_filtered[4]
            )
        )
        fig_ni_diff_per_year.add_trace(
            go.Box(
                x=df_filtered[5],
                y=df_filtered[1],
                name=lab,
                boxmean=True
            )
        )

    fig_fe_diff_per_shipment.update_layout(
        legend_title_text='Discharge Assay Lab',
        title='Iron Assay Difference per Shipment',
        xaxis_title='Loading Completion',
        yaxis_title='%Fe Difference<br>Loading - Discharging'
    )
    fe_diff_per_shipment = plot(fig_fe_diff_per_shipment, output_type='div')
    fig_fe_diff_per_year.update_layout(
        legend_title_text='Discharge Assay Lab',
        title='Iron Assay Difference per Year',
        xaxis_title='Year',
        yaxis_title='%Fe Difference<br>Loading - Discharging',
        boxmode='group'
    )
    fe_diff_per_year = plot(fig_fe_diff_per_year, output_type='div')
    fig_ni_diff_per_shipment.update_layout(
        legend_title_text='Discharge Assay Lab',
        title='Nickel Assay Difference per Shipment',
        xaxis_title='Loading Completion',
        yaxis_title='%Ni Difference<br>Loading - Discharging'
    )
    ni_diff_per_shipment = plot(fig_ni_diff_per_shipment, output_type='div')
    fig_ni_diff_per_year.update_layout(
        legend_title_text='Discharge Assay Lab',
        title='Nickel Assay Difference per Year',
        xaxis_title='Year',
        yaxis_title='%Ni Difference<br>Loading - Discharging',
        boxmode='group'
    )
    ni_diff_per_year = plot(fig_ni_diff_per_year, output_type='div')

    return render(request, 'sampling/index.html', {
        'fe_diff_per_shipment': fe_diff_per_shipment,
        'fe_diff_per_year': fe_diff_per_year,
        'ni_diff_per_shipment': ni_diff_per_shipment,
        'ni_diff_per_year': ni_diff_per_year
    })

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
        filename = os.path.join(tempdir, f'{assay.shipment.name}.tex')
        with open(filename, 'x', encoding='utf-8') as f:
            f.write(rendered_tpl)
        latex_command = f'cd "{tempdir}" && pdflatex --shell-escape ' + \
            f'-interaction=batchmode {os.path.basename(filename)}'
        run(latex_command, shell=True, stdout=PIPE, stderr=PIPE)
        run(latex_command, shell=True, stdout=PIPE, stderr=PIPE)
        return FileResponse(
            open(os.path.join(tempdir, f'{assay.shipment.name}.pdf'), 'rb'),
            content_type='application/pdf'
        )
