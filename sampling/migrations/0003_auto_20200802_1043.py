# Generated by Django 3.0.7 on 2020-08-02 02:43

from django.db import migrations
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('sampling', '0002_auto_20200801_2321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='approvedshipmentloadingassay',
            options={'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('approved'), nulls_first=True), '-assay__shipment__laydaysstatement__completed_loading']},
        ),
    ]
