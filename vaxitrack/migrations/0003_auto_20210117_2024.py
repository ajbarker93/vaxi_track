# Generated by Django 3.1.5 on 2021-01-17 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaxitrack', '0002_auto_20210117_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='assigned_centre',
            field=models.IntegerField(null=True),
        ),
    ]
