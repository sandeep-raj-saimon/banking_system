# Generated by Django 4.2.1 on 2023-05-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walletservice', '0007_alter_wallet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]
