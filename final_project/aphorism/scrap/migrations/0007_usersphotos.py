# Generated by Django 4.0.4 on 2022-05-26 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scrap', '0006_alter_messege_sender'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('is_main', models.BooleanField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='users_photos_media')),
                ('date', models.DateTimeField(auto_now=True)),
                ('user_photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
