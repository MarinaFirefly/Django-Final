# Generated by Django 2.2 on 2020-07-03 21:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0003_seance_is_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seance',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]