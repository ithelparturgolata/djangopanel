# Generated by Django 5.1.1 on 2024-10-18 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0020_alter_budynek_kod_alter_historicalbudynek_kod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budynek',
            name='laczna_powierzchnia_dzialki',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='budynek',
            name='powierzchnia_wspolna_budynku',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='historicalbudynek',
            name='laczna_powierzchnia_dzialki',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='historicalbudynek',
            name='powierzchnia_wspolna_budynku',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
