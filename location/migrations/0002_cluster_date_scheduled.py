# Generated by Django 3.0.3 on 2020-02-29 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='date_scheduled',
            field=models.DateField(blank=True, help_text='Scheduled date of start of excavation', null=True),
        ),
    ]