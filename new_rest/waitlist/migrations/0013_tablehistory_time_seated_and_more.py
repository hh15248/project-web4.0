# Generated by Django 4.0.3 on 2022-05-03 02:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('waitlist', '0012_alter_wait_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablehistory',
            name='time_seated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='waitlisthistory',
            name='arrival_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
