# Generated by Django 2.0.2 on 2018-06-21 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('air', '0006_auto_20180621_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steam_player_bans',
            name='communitybanned',
            field=models.CharField(max_length=225),
        ),
        migrations.AlterField(
            model_name='steam_player_bans',
            name='vacbanned',
            field=models.CharField(max_length=225),
        ),
    ]
