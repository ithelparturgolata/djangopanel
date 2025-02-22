# Generated by Django 5.1.1 on 2024-10-10 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0013_budynek_telefon_osiedla'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budynek',
            name='osiedle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='budynki', to='panel.administracjaosiedla'),
        ),
        migrations.AlterField(
            model_name='budynek',
            name='spoldzielnia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='budynki', to='panel.spoldzielnia'),
        ),
    ]
