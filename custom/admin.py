from django.contrib.admin import ModelAdmin, TabularInline, register
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Log, MobileNumber, User


class MobileNumberInline(TabularInline):
    fields = ('user', 'number')
    model = MobileNumber
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
                'sex',
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
    inlines = [MobileNumberInline]


class ReadOnlyAdmin(ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
