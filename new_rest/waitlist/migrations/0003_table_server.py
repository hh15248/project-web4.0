# Generated by Django 4.0.3 on 2022-04-29 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waitlist', '0002_table_remove_wait_dining_time_remove_wait_left_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='server',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
