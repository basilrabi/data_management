# Generated by Django 3.1.2 on 2020-10-29 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='block',
            index=models.Index(fields=['exposed', 'fe', 'ni', 'z', 'planned_excavation_date'], name='inventory_b_exposed_350d62_idx'),
        ),
    ]