from django.contrib.admin import ModelAdmin, register

from .models import OutgoingCommunication, ExternalIncomingCommunication
from organization.models import Division


@register(OutgoingCommunication)
class OutgoingCommunicationAdmin(ModelAdmin):
    date_hierarchy = 'date'
    fields = ('date',
              'nature_of_content',
              'recipient',
              'original_copy',
              'receiving_copy',
              'cancel',)

    list_display = ('date',
                    'transmittal_number',
                    'content',
                    'recipient_render',
                    'original_copy',
                    'receiving_copy'
    )

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
