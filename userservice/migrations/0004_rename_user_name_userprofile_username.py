# Generated by Django 4.2.1 on 2023-05-04 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userservice', '0003_alter_userprofile_managers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_name',
            new_name='username',
        ),
    ]