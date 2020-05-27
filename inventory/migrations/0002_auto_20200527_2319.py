# Generated by Django 3.0.6 on 2020-05-27 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='excavated',
        ),
        migrations.AddField(
            model_name='block',
            name='depth',
            field=models.FloatField(blank=True, help_text='Distance of the centroid from the surface. A positive\n        value means that the centroid is still below the surface.\n        ', null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='co',
            field=models.FloatField(help_text='Estimated cobalt content of the block in percent.'),
        ),
        migrations.AlterField(
            model_name='block',
            name='fe',
            field=models.FloatField(help_text='Estimated iron content of the block in percent.'),
        ),
        migrations.AlterField(
            model_name='block',
            name='ni',
            field=models.FloatField(help_text='Estimated nickel content of the block in percent.'),
        ),
        migrations.AlterField(
            model_name='block',
            name='z',
            field=models.SmallIntegerField(help_text='Elevation of the top face of the block.'),
        ),
    ]
