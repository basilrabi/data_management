from django.contrib.admin import ModelAdmin, register

from .models import OutgoingCommunication, ExternalIncomingCommunication, Letter, PoliciesAndGuideline
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
                    'nature_of_content',
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


@register(Letter)
class LetterAdmin(ModelAdmin):
    date_hierarchy = 'date'
    fields = ('date',
              'nature_of_content',
              'recipient',
              'original_copy',
              'receiving_copy',
              'cancel',)

    list_display = ('date',
                    'transmittal_number',
                    'nature_of_content',
                    'recipient_render',
                    'original_copy',
                    'receiving_copy'
    )

    ordering = ('-date', '-transmittal_number')


@register(PoliciesAndGuideline)
class PoliciesAndGuidelineAdmin(ModelAdmin):
    date_hierarchy = 'date'
    fields = ('date',
              'nature_of_content',
              'concerned_personnel',
              'date_of_effectivity',
              'date_of_expiry',
              'signed_copy',
              'cancel',)

    list_display = ('date',
                    'transmittal_number',
                    'nature_of_content',
                    'concerned_personnel',
                    'date_of_effectivity',
                    'date_of_expiry',
                    'signed_copy'
    )

    ordering = ('-date', '-transmittal_number')