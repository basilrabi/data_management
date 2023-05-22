from django.contrib.admin import ModelAdmin, register

from .models import ExternalCommunication


@register(ExternalCommunication)
class ExternalCommunicationAdmin(ModelAdmin):
    fields = ('date',
              'nature_of_content',
              'receiving_copy',)

    list_display = ('transmittal_number',
                    'receiving_copy'
    )
