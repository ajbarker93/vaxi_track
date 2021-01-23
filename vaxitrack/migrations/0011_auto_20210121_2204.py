# Generated by Django 3.1.5 on 2021-01-21 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaxitrack', '0010_logf'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LogF',
        ),
        migrations.DeleteModel(
            name='Reg',
        ),
        migrations.DeleteModel(
            name='UserF',
        ),
        migrations.AddField(
            model_name='centre',
            name='VaxiTrack_ID',
            field=models.CharField(default='123456', max_length=10),
        ),
        migrations.AddField(
            model_name='centre',
            name='available_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='centre',
            name='centre_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='centre',
            name='vax_type',
            field=models.CharField(default='', max_length=30),
        ),
    ]
