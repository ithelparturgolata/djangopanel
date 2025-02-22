# Generated by Django 5.1.1 on 2024-11-06 04:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0025_alter_historicalremonty_opis_remontu_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code_image', models.ImageField(blank=True, null=True, upload_to='qr_codes/')),
                ('budynek', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='qrcode', to='panel.budynek')),
            ],
        ),
    ]
