# Generated by Django 4.0.3 on 2022-04-29 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waitlist', '0005_alter_table_time_seated_alter_wait_arrival_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='time_seated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='wait',
            name='arrival_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
