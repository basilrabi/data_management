from django.contrib.admin import ModelAdmin, register
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import MapDocumentControl, MapType, MinePlanningEngineer
from .forms import MapDocumentControlForm

@register(MapDocumentControl)
class MapDocumentControlAdmin(ModelAdmin):
    form = MapDocumentControlForm
    list_display = (
        'reference_map_no', 'map_title','date_created',
        'short_map_uploads_img', 'short_map_uploads_zip',
        'map_creator'
    )
    list_filter = ('map_type', 'ridge', 'company', 'month')
    readonly_fields = ('number', 'revision',)

    # Define a short link for map_uploads_img
    def short_map_uploads_img(self, obj):
        if obj.map_uploads_img:
            return format_html(
                '<a href="{}" target="_blank">Map File</a>',
                obj.map_uploads_img.url
            )
        return "-"
    short_map_uploads_img.short_description = "Map Upload (Image)"

    # Define a short link for map_uploads_zip
    def short_map_uploads_zip(self, obj):
        if obj.map_uploads_zip:
            return format_html(
                '<a href="{}" target="_blank">Map File</a>',
                obj.map_uploads_zip.url
            )
        return "-"
    short_map_uploads_zip.short_description = "Map Upload (ZIP)"

    # Define the action
    actions = ['duplicate_map_document']

    def duplicate_map_document(self, request, queryset):
        """
        Custom admin action to duplicate selected MapDocumentControl entries.
        """
        if queryset.count() > 1:
            messages.warning(request, _("You can only duplicate one item at a time."))
            return

        for obj in queryset:
            # Duplicate the object
            obj.pk = None  # Reset primary key to create a new instance
            obj.revision = 0  # Reset revision to 0 for the new entry

            # Automatically generate a new `number`
            count = MapDocumentControl.objects.filter(
                map_type=obj.map_type,
                year_on_map=obj.year_on_map
            ).count()
            obj.number = str(count + 1).zfill(3)

            # Save the duplicated object
            obj.save()

        messages.success(request, _("Selected MapDocumentControl entry has been duplicated."))

    duplicate_map_document.short_description = "Duplicate selected Map Document"

@register(MapType)
class MapTypeAdmin(ModelAdmin):
    pass

@register(MinePlanningEngineer)
class MinePlanningEngineerAdmin(ModelAdmin):
    pass
