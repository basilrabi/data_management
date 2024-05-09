from django.contrib.admin import ModelAdmin, register

from .models import ExternalCommunication, ExternalIncomingCommunication
from organization.models import Division


@register(ExternalCommunication)
class ExternalCommunicationAdmin(ModelAdmin):
    date_hierarchy = 'date'
    fields = ('date',
              'nature_of_content',
              'requesting_department',
              'recipient',
              'receiving_copy',
              'cancel',)

    list_display = ('date',
                    'transmittal_number',
                    'content',
                    'recipient_render',
                    'receiving_copy',
                    'requesting_department'
    )
    list_filter = ['requesting_department']
    ordering = ('-date', '-transmittal_number')


@register(ExternalIncomingCommunication)
class ExternalIncomingCommunicationAdmin(ModelAdmin):

    date_hierarchy = 'datetime_received'
    fields = ('datetime_received',
              'subject',
              'sender',
              'scan',)

    list_display = ('transmittal_number',
                    'datetime_received',
                    'subject',
                    'sender',
                    'scan'
    )
    ordering = ('-datetime_received', '-transmittal_number')
