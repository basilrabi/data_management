# Generated by Django 4.0.4 on 2022-05-10 05:31

import custom.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentmodel',
            name='name',
            field=custom.fields.NameField(max_length=40),
        ),
    ]
