# Generated by Django 2.2 on 2020-07-02 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seance',
            options={'ordering': ['start_day', 'start_time']},
        ),
    ]