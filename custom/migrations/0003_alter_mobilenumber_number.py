# Generated by Django 4.0.4 on 2022-04-22 15:10

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0002_mobilenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobilenumber',
            name='number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True),
        ),
    ]
