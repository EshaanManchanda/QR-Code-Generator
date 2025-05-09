# Generated by Django 5.1.7 on 2025-04-01 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrcode',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
        migrations.AddField(
            model_name='qrcode',
            name='logo_size',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AddField(
            model_name='qrcode',
            name='transparent_background',
            field=models.BooleanField(default=False),
        ),
    ]
