# Generated by Django 3.0.6 on 2020-05-30 01:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20200529_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='repeat',
            field=models.BooleanField(default=False, help_text='Можно ли повторять опрос'),
        ),
        migrations.AddField(
            model_name='poll',
            name='repeat_pause',
            field=models.DurationField(default=datetime.timedelta(days=1), help_text='как часто можно повторять опрос'),
        ),
    ]
