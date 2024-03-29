# Generated by Django 4.2.7 on 2023-12-18 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_userprofile_restaurant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(blank=True, choices=[('customer', 'Customer'), ('restaurant', 'Restaurant')], max_length=20),
        ),
    ]
