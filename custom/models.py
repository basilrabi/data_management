from django.contrib.auth.models import AbstractUser, Group
from django.contrib.gis.db.models import (Model as GeoModel, MultiPolygonField)
from django.db.models import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    F,
    ForeignKey,
    ManyToManyField,
    Model,
    PositiveSmallIntegerField,
    SET_NULL,
    TextField
)
from phonenumber_field.modelfields import PhoneNumberField

from custom.fields import NameField, SpaceLess
from custom.functions_standalone import print_tz_manila



class Classification(Model):
    """
    Template for any classification.
    """
    name = NameField(max_length=40, unique=True)
    description = TextField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class FixedAsset(Model):
    """
    Template for fixed asset non-changing data
    """
    
    acquisition_cost = DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2,
        help_text='Cost in Philippine Peso as recorded by TSD'
    )
    acquisition_cost_from_accounting = DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2,
        help_text='Cost in Philippine Peso'
    )
    date_acquired = DateField(null=True, blank=True)
    date_phased_out = DateField(null=True, blank=True)
    asset_tag_id = NameField(max_length=20, null = True, blank = True)
    asset_serial_number = NameField(max_length=20, null = True, blank = True)
    asset_code = NameField(max_length=20, null = True, blank = True, help_text="SAP ID")
    service_life = PositiveSmallIntegerField(null=True, blank=True, help_text = "No. of months")
    description = TextField(max_length = 50, null=True, blank=True)
    active = BooleanField(default=True)

    class Meta:
        abstract = True



class GeoClassification(GeoModel):
    """
    Template for any classification.
    """
    name = NameField(max_length=40, unique=True)
    description = TextField(null=True, blank=True)
    geom = MultiPolygonField(srid=3125)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Log(Model):
    """
    Asyncronous log storage
    """
    created = DateTimeField(auto_now_add=True)
    log = TextField()

    class Meta:
        ordering = [F('created').desc()]


class MobileNumber(Model):
    user = ForeignKey('User', null=True, blank=True, on_delete=SET_NULL)
    number = PhoneNumberField(unique=True)
    spaceless_number = SpaceLess(
        null=True, blank=True, unique=True, max_length=20
    )

    def save(self, *args, **kwargs):
        self.spaceless_number = self.number
        super().save(*args, **kwargs)

    class Meta:
        ordering = [F('user__username').asc(), F('spaceless_number').asc()]

    def __str__(self):
        return f'{self.number.as_international} {self.user}'


class TextMessage(Model):
    """
    SMS to be sent to either a number, user, or a group. SMS is sent once saved.
    """
    NUMBER_CHOICES = (
        ('222', '222'),
        ('8080', '8080')
    )
    provider_number = CharField(
        null=True,
        blank=True,
        max_length=4,
        choices=NUMBER_CHOICES,
        help_text='If this field is set, the number and group fields are ignored. This is used in sending SMS to the network provider.'
    )
    number = ManyToManyField(
        'MobileNumber',
        blank=True,
        help_text='If this field is not empty, the group field is ignored.<br/>'
    )
    group = ManyToManyField(
        Group,
        blank=True,
        help_text='If either provider_number or number field is not empty, this field is ignored.<br/>'
    )
    sms = TextField(
        null=True,
        blank=True,
        help_text='Text message to be sent. Message shall only be sent if recipient is not empty.'
    )
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)
    user = ForeignKey('User', blank=True, null=True, on_delete=SET_NULL)

    def _recipient(self) -> set[str]:
        numbers = set()
        if self.provider_number:
            numbers.add(self.provider_number)
        elif self.number.all().exists():
            for number in self.number.all():
                numbers.add(number.spaceless_number)
        elif self.group.all().exists():
            for group in self.group.all():
                for user in group.user_set.all():
                    for number in user.mobilenumber_set.all():
                        numbers.add(number.spaceless_number)
        return numbers

    def recipient(self) -> (str | None):
        recipients = self._recipient()
        if recipients:
            return '\n'.join(recipients)

    class Meta:
        ordering = [F('modified').desc()]

    def __str__(self) -> str:
        if self.modified:
            sms = self.sms or 'Empty'
            if self.user:
                return f'{print_tz_manila(self.modified)[:19]} - {self.user} - {sms[:30]}'
            return f'{print_tz_manila(self.modified)[:19]} {sms[:40]}'
        return 'New'


class User(AbstractUser):
    middle_name = CharField(null=True, blank=True, max_length=100)
    birth_date = DateField(null=True, blank=True)
    name_suffix = NameField(
        max_length=20,
        null=True,
        blank=True,
        help_text='Junior, Senior, III, etc.'
    )

    SEX_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('N', 'Non-binary')
    )
    sex = CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)

    def middle_initial(self):
        if self.middle_name:
            mi = [x[:1].upper() for x in str(self.middle_name).split(' ')]
            return '.'.join(mi) + '.'
        return ''
