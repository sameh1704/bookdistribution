# Generated by Django 5.0.6 on 2024-06-17 17:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_bookletoutstore_class_level_bookletoutstore_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookletdelivery',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.supplier', verbose_name='المورد'),
        ),
    ]
