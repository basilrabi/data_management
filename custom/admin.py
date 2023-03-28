from django.contrib.admin import ModelAdmin, TabularInline, register
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import (
    Log,
    MobileNumber,
    Profession,
    ProfessionalIdentificationCard,
    TextMessage,
    User
)


class MobileNumberInline(TabularInline):
    fields = ('user', 'number')
    model = MobileNumber
    extra = 0


class ProfessionalIdentificationCardInline(TabularInline):
    fields = (
        'holder', 'number', 'profession', 'date_registered', 'date_expiry'
    )
    model = ProfessionalIdentificationCard
    extra = 0


@register(Log)
class LogAdmin(ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('created', 'log')
    readonly_fields = ['created', 'log']


@register(MobileNumber)
class MobileNumberAdmin(ModelAdmin):
    fields = ('user', 'number')
    list_display = ('user', 'number')
    search_fields = ('user__username', 'spaceless_number')


@register(TextMessage)
class TextMessageAdmin(ModelAdmin):
    date_hierarchy = 'modified'
    exclude = ['user']
    fieldsets = (
        (None, {'fields': ('sms', 'recipient')}),
        (None, {'fields': ('created', 'modified', 'user')}),
        ('Provider Options', {
            'classes': ('collapse',),
            'fields': ('provider_number',)
        }),
        ('Single Recipients', {
            'classes': ('collapse',),
            'fields': ('number',)
        }),
        ('Group Recipients', {
            'classes': ('collapse',),
            'fields': ('group',)
        })
    )
    filter_horizontal = ('number', 'group')
    readonly_fields = ('created', 'modified', 'recipient','user')
    search_fields = ('sms',)

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return super().get_queryset(request).filter(user=request.user)
        return super().get_queryset(request)

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        obj.user = request.user
        return obj


@register(Profession)
class ProfessionAdmin(ModelAdmin):
    pass


@register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
                'email',
                'birth_date',
                'sex'
            )
        }),
        (_('Permissions'), {
            'fields': ('is_active',
                       'is_staff',
                       'is_superuser',
                       'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', 'user_permissions')
    inlines = [MobileNumberInline, ProfessionalIdentificationCardInline]


class ReadOnlyAdmin(ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
