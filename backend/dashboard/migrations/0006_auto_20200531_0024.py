# Generated by Django 3.0.6 on 2020-05-30 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20200530_0436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poll',
            options={'ordering': ['pk'], 'verbose_name': 'Опрос', 'verbose_name_plural': 'Опросы'},
        ),
        migrations.AlterModelOptions(
            name='results',
            options={'ordering': ['-created_time'], 'verbose_name': 'Результат', 'verbose_name_plural': 'Результаты'},
        ),
    ]