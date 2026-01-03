from django.contrib.admin import ModelAdmin, register

from .models import OutgoingCommunication, ExternalIncomingCommunication, Letter, PoliciesAndGuideline
from organization.models import Division

from django.urls import reverse
from django.utils.html import format_html


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
    
    search_fields = ['transmittal_number', 'nature_of_content']

    fields = (
        'date',
        'nature_of_content',
        'concerned_personnel',
        'update_existing',
        'date_of_effectivity',
        'date_of_expiry',
        'signed_copy',
        'cancel',
    )

    autocomplete_fields = ['update_existing']

    list_display = (
        'date',
        'transmittal_number',
        'nature_of_content',
        'concerned_personnel',
        'date_of_effectivity',
        'date_of_expiry',
        'signed_copy',
        'get_update_existing_link' 
    )

    ordering = ('-date', '-transmittal_number')

    def get_update_existing_link(self, obj):
        if obj.update_existing:
            app_label = obj._meta.app_label
            model_name = obj._meta.model_name
            view_name = f"admin:{app_label}_{model_name}_change"
            
            link_url = reverse(view_name, args=[obj.update_existing.pk])
            
            return format_html('<a href="{}">{}</a>', link_url, obj.update_existing)
        
        return "-"

    get_update_existing_link.short_description = 'Update Existing'