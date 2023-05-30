from django.contrib.admin import ModelAdmin, register

from .models import ExternalCommunication
from organization.models import Division


@register(ExternalCommunication)
class ExternalCommunicationAdmin(ModelAdmin):
    
    fields = ('date',
              'nature_of_content',
              'requesting_department',
              'recipient',
              'receiving_copy',
              'cancel',)

    list_display = ('transmittal_number',
                    'content',
                    'recipient_render',
                    'receiving_copy',
                    'requesting_department'
    )    