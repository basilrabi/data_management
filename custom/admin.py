from django.contrib.admin import ModelAdmin, TabularInline, register
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import MobileNumber, User


class MobileNumberInline(TabularInline):
    model = MobileNumber
    extra = 0


@register(MobileNumber)
class MobileNumberAdmin(ModelAdmin):
    pass


@register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
            {'fields': ('first_name', 'middle_name', 'last_name', 'email')}
        ),
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
