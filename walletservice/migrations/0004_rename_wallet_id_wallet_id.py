# Generated by Django 4.2.1 on 2023-05-04 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walletservice', '0003_remove_wallet_id_wallet_wallet_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='wallet_id',
            new_name='id',
        ),
    ]