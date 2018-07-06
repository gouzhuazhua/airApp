# Generated by Django 2.0.2 on 2018-06-14 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='steam_news',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('url', models.CharField(max_length=225)),
                ('author', models.CharField(max_length=225)),
                ('contents', models.CharField(max_length=225)),
                ('date', models.DateField()),
                ('appid', models.IntegerField()),
            ],
        ),
    ]
