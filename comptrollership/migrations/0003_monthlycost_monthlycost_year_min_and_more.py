# Generated by Django 4.2 on 2023-05-04 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptrollership', '0002_alter_sapcostcenter_long_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='monthlycost',
            constraint=models.CheckConstraint(check=models.Q(('year__gte', 2021)), name='monthlycost_year_min'),
        ),
        migrations.AddConstraint(
            model_name='monthlycost',
            constraint=models.CheckConstraint(check=models.Q(('month__gte', 1)), name='monthlycost_month_min'),
        ),
        migrations.AddConstraint(
            model_name='monthlycost',
            constraint=models.CheckConstraint(check=models.Q(('month__lte', 13)), name='monthlycost_month_max'),
        ),
    ]
