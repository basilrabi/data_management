from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    FileField,
    ForeignKey,
    IntegerField,
    Max,
    Model,
    PROTECT,
    TextField
)
from django import forms

from organization.models import Organization

# Create your models here.

def filepath(instance, filename):
    filename = f"{instance.reference_map_no}.png"
    return f"mine_planning/map_uploads/{instance.year_on_map}/{filename}"

def filepath_zip(instance, filename):
    filename = f"{instance.reference_map_no}.zip"
    return f"mine_planning/map_uploads/{instance.year_on_map}/pdf/{filename}"

class MapType(Model):

    map_type = CharField(
        max_length=40, null=True, blank=False
    )
 
    map_prefix = CharField(
        max_length=40, null=True, blank=False
    )

    def __str__(self):
        return self.map_type

class MinePlanningEngineer(Model):
    
    full_name = CharField(
        max_length=40, null=True, blank=True
    )
    def __str__(self):
        return self.full_name

class MapDocumentControl(Model):

    material_choices = (
        ('SAP', 'Saprolite'),
        ('LIM', 'Limonite')
    )

    ridge_choices = (
        ('', ''),
        ('ALL_', 'ALL Ridges'),
        ('CA_', 'Cagdianao'),
        ('HY_', 'Haya'),
        ('T1_', 'Taga 1'),
        ('T2_', 'Taga 2'),
        ('T3_', 'Taga 3'),
        ('UR_', 'Urbiz'),
    )

    month_choices = (
        ('Jan', 'January'),
        ('Feb', 'February'),
        ('Mar', 'March'),
        ('Apr', 'April'),
        ('May', 'May'),
        ('Jun', 'June'),
        ('Jul', 'July'),
        ('Aug', 'August'),
        ('Sep', 'September'),
        ('Oct', 'October'),
        ('Nov', 'November'),
        ('Dec', 'December')
    )

    week_choices = (
        ('W1', 'Week 1'),
        ('W2', 'Week 2'),
        ('W3', 'Week 3'),
        ('W4', 'Week 4')
    )

    map_title = TextField(
        max_length=100, null=True, blank=True
    )

    date_created = DateField(
        null = True, blank=False
    )

    map_type = ForeignKey(
        MapType, on_delete=PROTECT, null=True
    )

    material = CharField(
        max_length=3, choices=material_choices, null=True, blank=True
    )

    company = ForeignKey(
        Organization, on_delete=PROTECT, null=True, blank=True
    )

    ridge = CharField(
        max_length=10, default='', choices=ridge_choices, null=False, blank=True
    )

    mineblock = CharField(
        max_length=30, null=True, blank=True
    )

    year_on_map = CharField(
        max_length=4, null=True, blank=False
    )

    month = CharField(
        max_length=9, choices=month_choices, default='', null=True, blank=True
    )

    week_start = CharField(
        max_length=2, choices=week_choices, default='', null=True, blank=True
    )

    week_end = CharField(
        max_length=2, choices=week_choices, default='', null=True, blank=True
    )

    bench = CharField(
        max_length=30, null=True, blank=True
    )

    number = CharField(
        max_length=3, null=False, blank=True
    )

    revision = IntegerField(
        default=0, null=False, blank=False
    )

    revised_from = ForeignKey(
        'self', on_delete=PROTECT, null=True, blank=True
    )

    revision_notes = TextField(
        max_length = 256, null=False, blank=True
    )

    map_uploads_img = FileField(
        upload_to=filepath, null=True, blank=True
    )

    map_uploads_zip = FileField(
        upload_to=filepath_zip, null=True, blank=True
    )

    map_creator = ForeignKey(
        MinePlanningEngineer, on_delete=PROTECT, null=True, blank=True
    )

    @property
    def reference_map_no(self):
        return f"{self.map_type.map_prefix}_{self.ridge}{self.number}_{self.year_on_map}"
        
    def save(self, *args, **kwargs):
        if not self.revision: 
            if self.revised_from:
                self.revision = self.revised_from.revision + 1
            else:
                self.revision = 0

        should_calculate = False
        
        if self.pk:
            old_data = MapDocumentControl.objects.filter(pk=self.pk).values('map_type', 'ridge', 'year_on_map').first()
            if old_data:
                if (old_data['map_type'] != self.map_type_id or 
                    old_data['ridge'] != self.ridge or 
                    old_data['year_on_map'] != self.year_on_map):
                    should_calculate = True
        else:
            should_calculate = True

        if should_calculate:
            res = MapDocumentControl.objects.filter(
                map_type=self.map_type, 
                year_on_map=self.year_on_map,
                ridge=self.ridge
            ).exclude(pk=self.pk).aggregate(Max('number'))

            max_num_str = res.get('number__max')

            if max_num_str and max_num_str.isdigit():
                new_num = int(max_num_str) + 1
            else:
                new_num = 1

            self.number = str(new_num).zfill(3)

        super(MapDocumentControl, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.reference_map_no