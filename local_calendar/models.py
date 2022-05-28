from django.db.models import CharField, DateField, ForeignKey, Model, PROTECT

from custom.models import Classification


class Holiday(Model):
    HOLIDAY_CHOICES = (
        ('LH', 'Legal Holiday'),
        ('NH', 'Negotiated Holiday'),
        ('SH', 'Special Holiday')
    )
    date = DateField()
    event = ForeignKey('HolidayEvent', on_delete=PROTECT)
    type = CharField(max_length=2, choices=HOLIDAY_CHOICES)

    class Meta:
        ordering = ['date', 'event']

    def __str__(self) -> str:
        return f'{self.date} {self.event}'


class HolidayEvent(Classification):
    pass
