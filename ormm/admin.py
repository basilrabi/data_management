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


@register(ExternalIncomingCommunication)    
class ExternalIncomingCommunicationAdmin(ModelAdmin):

    list_display = ('subject',
                    'sender',
                    'datetime_received',
                    'scan'
    )
