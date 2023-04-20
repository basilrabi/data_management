# Generated by Django 4.1.7 on 2023-03-24 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_department_division_section_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='parent_division',
            new_name='parent_department',
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
    ]