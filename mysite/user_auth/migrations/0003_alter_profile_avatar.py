# Generated by Django 4.0.6 on 2024-09-26 08:27

from django.db import migrations, models
import user_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=user_auth.models.generate_profile_images_path),
        ),
    ]
