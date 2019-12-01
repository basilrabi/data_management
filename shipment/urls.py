from django.urls import path

from . import views

urlpatterns = [
    path(
        'statement/<slug:name>',
        views.lay_days_statement_pdf,
        name='lay-days-pdf'
    )
]
