# Generated by Django 3.1.5 on 2021-01-22 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaxitrack', '0011_auto_20210121_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centre',
            name='VaxiTrack_ID',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.CharField(max_length=10),
        ),
    ]
