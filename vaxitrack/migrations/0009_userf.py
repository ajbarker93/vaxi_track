# Generated by Django 3.1.5 on 2021-01-21 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaxitrack', '0008_auto_20210120_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30)),
                ('Post_Code', models.CharField(max_length=30)),
                ('Email', models.CharField(max_length=40)),
                ('Age', models.CharField(max_length=10)),
            ],
        ),
    ]
