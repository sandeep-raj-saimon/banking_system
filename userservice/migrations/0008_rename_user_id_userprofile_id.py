# Generated by Django 4.2.1 on 2023-05-04 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userservice', '0007_alter_userprofile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_id',
            new_name='id',
        ),
    ]
