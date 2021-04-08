# Generated by Django 3.1.7 on 2021-03-13 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='dumping_area',
            field=models.ForeignKey(blank=True, help_text='Assigned dumping area.', null=True, on_delete=django.db.models.deletion.PROTECT, to='location.stockpile'),
        ),
    ]