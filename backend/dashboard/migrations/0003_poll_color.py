# Generated by Django 3.0.6 on 2020-05-24 22:44

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20200525_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', help_text='Цвет блока', max_length=18),
        ),
    ]
