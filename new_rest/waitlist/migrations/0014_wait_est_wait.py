# Generated by Django 4.0.3 on 2022-05-03 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waitlist', '0013_tablehistory_time_seated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wait',
            name='est_wait',
            field=models.IntegerField(default=0),
        ),
    ]
