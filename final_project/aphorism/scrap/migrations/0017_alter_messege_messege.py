# Generated by Django 4.0.4 on 2022-06-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0016_friends_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messege',
            name='messege',
            field=models.TextField(blank=True, null=True),
        ),
    ]