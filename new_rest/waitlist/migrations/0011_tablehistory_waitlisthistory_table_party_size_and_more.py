# Generated by Django 4.0.3 on 2022-05-02 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waitlist', '0010_remove_config_number_of_servers'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('party', models.CharField(default='Empty', max_length=20)),
                ('party_size', models.IntegerField()),
                ('server', models.CharField(default='None', max_length=20)),
                ('dining_time', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='WaitlistHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('party_size', models.CharField(max_length=20)),
                ('wait_time', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='table',
            name='party_size',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wait',
            name='name',
            field=models.CharField(max_length=120),
        ),
    ]