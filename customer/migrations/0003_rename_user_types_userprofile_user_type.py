# Generated by Django 4.2.7 on 2023-12-04 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_userprofile_managers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_types',
            new_name='user_type',
        ),
    ]