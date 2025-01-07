from django.contrib.admin import ModelAdmin, register
from .models import MapDocumentControl, MapType, MinePlanningEngineer
from .forms import MapDocumentControlForm

from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from django.contrib import messages
from django.utils.translation import gettext_lazy as _

@register(MapDocumentControl)
class MapDocumentControlAdmin(ModelAdmin):
    form = MapDocumentControlForm
    list_display = ('reference_map_no', 'date_created', 'material', 'ridge', 'year_on_map', 'month', 'company', 'map_uploads_img', 'map_creator', 'revision')
    list_filter = ('map_type', 'ridge', 'company', 'month')
    readonly_fields = ('number', 'revision',)

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
            count = MapDocumentControl.objects.filter(map_type=obj.map_type, year_on_map=obj.year_on_map).count()
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

