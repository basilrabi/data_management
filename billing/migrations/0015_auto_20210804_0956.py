# Generated by Django 3.1.11 on 2021-08-04 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0014_savefile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='saveFile',
        ),
        migrations.AlterField(
            model_name='billingtracker',
            name='fileup',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]