# Generated by Django 5.0.6 on 2024-06-17 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_bookoutstore_class_level_bookoutstore_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookletoutstore',
            name='class_level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.classlevel', verbose_name='الصف الدراسي'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookletoutstore',
            name='stage',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.stage', verbose_name='المرحلة الدراسية'),
            preserve_default=False,
        ),
    ]
