# Generated by Django 5.1.7 on 2025-04-01 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr', '0002_qrcode_logo_qrcode_logo_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrcode',
            name='border_style',
            field=models.CharField(choices=[('solid', 'Solid'), ('dashed', 'Dashed'), ('dotted', 'Dotted')], default='solid', max_length=20, verbose_name='Border Style'),
        ),
        migrations.AddField(
            model_name='qrcode',
            name='logo_position',
            field=models.CharField(choices=[('center', 'Center'), ('top-left', 'Top Left'), ('top-right', 'Top Right'), ('bottom-left', 'Bottom Left'), ('bottom-right', 'Bottom Right')], default='center', max_length=20, verbose_name='Logo Position'),
        ),
    ]
