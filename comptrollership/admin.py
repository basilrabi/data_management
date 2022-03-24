from django.contrib.admin import ModelAdmin, register

from .models import SapCostCenter, Question, Choice, TestImporter

@register(SapCostCenter)
class SapCostCenterAdmin(ModelAdmin):
    pass

@register(Question)
class Question(ModelAdmin):
    pass

@register(Choice)
class Choice(ModelAdmin):
    pass

@register(TestImporter)
class TestImporter(ModelAdmin):
    pass
