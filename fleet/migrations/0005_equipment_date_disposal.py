# Generated by Django 4.1.7 on 2023-03-09 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0004_equipment_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='date_disposal',
            field=models.DateField(blank=True, null=True),
        ),
    ]
