# Generated by Django 4.0 on 2022-03-24 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0018_auto_20210814_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddon',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='billingtracker',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
