from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    CheckConstraint,
    DateField,
    ForeignKey,
    Model,
    PositiveSmallIntegerField,
    Q
)

from custom.fields import NameField


class PilingMethod(Model):
    name = NameField(max_length=20, unique=True)

    def trip(self, date):
        if self.tripsperpile_set.all().count() > 0:
            return self.tripsperpile_set.filter(
                Q(effectivity__lte=date),
                Q(end__gte=date) |
                Q(end__isnull=True)
            ).first().trips

    def present_required_trip(self):
        return self.trip(date.today())

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TripsPerPile(Model):
    piling_method = ForeignKey('PilingMethod', on_delete=CASCADE)
    effectivity = DateField()
    end = DateField(null=True, blank=True)
    trips = PositiveSmallIntegerField()

    def next(self):
        return self.piling_method.tripsperpile_set.filter(Q(
            effectivity__gt=self.effectivity
        )).order_by('effectivity').first()

    def previous(self):
        return self.piling_method.tripsperpile_set.filter(Q(
            effectivity__lt=self.effectivity
        )).order_by('-effectivity').first()

    def clean(self):
        if self.end:
            if self.end <= self.effectivity:
                raise ValidationError('Effectivity must be earlier than end.')
        if self.piling_method.tripsperpile_set.filter(
            Q(
                effectivity__lte=self.end or self.effectivity + timedelta(9999)
            ),
            Q(end__gte=self.effectivity) |
            Q(end__isnull=True)
        ).exclude(id=self.id).count() > 0:
            raise ValidationError('Effectivity should not overlap.')

        if self.next():
            if self.next().effectivity - self.end > timedelta(1):
                raise ValidationError('Effective dates must not have gaps.')

        if self.previous():
            if self.effectivity - self.previous().end > timedelta(1):
                raise ValidationError('Effective dates must not have gaps.')

    class Meta:
        ordering = ['-effectivity']
        constraints = [
            CheckConstraint(
                check=Q(trips__gt=0), name='trips_min_1'
            )
        ]
