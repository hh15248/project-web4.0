# Generated by Django 4.0.3 on 2022-04-29 02:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('waitlist', '0004_alter_table_time_seated_alter_wait_arrival_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='time_seated',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 29, 2, 38, 55, 590081, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='wait',
            name='arrival_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 29, 2, 38, 55, 589827, tzinfo=utc)),
        ),
    ]
