# Generated by Django 4.0.6 on 2022-08-20 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material_management', '0003_alter_unitofmeasure_options_alter_unitofmeasure_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valuation',
            name='name',
            field=models.PositiveSmallIntegerField(unique=True),
        ),
    ]
