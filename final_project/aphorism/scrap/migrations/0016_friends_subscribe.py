# Generated by Django 4.0.4 on 2022-06-01 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0015_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='subscribe',
            field=models.BooleanField(default=False),
        ),
    ]