# Generated by Django 3.1.5 on 2021-01-23 17:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaxitrack', '0014_auto_20210123_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='assigned_centre',
            new_name='assigned_centre_id',
        ),
        migrations.AddField(
            model_name='user',
            name='assigned_centre_name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='assigned_centre_postcode',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='centre',
            name='VaxiTrack_ID',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='centre',
            name='available_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='centre',
            name='doses_available',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='centre',
            name='vax_type',
            field=models.IntegerField(choices=[('0', 'Oxford-AZ'), ('1', 'Pfizer')], default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]