# Generated by Django 4.0.3 on 2022-03-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carga', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastRefresh',
            fields=[
                ('dataset_name', models.CharField(max_length=50)),
                ('dataset_id', models.CharField(max_length=255)),
                ('status', models.CharField(blank=True, max_length=25, null=True)),
                ('refresh_type', models.CharField(max_length=25)),
                ('request_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('history_id', models.CharField(max_length=255)),
                ('started_at', models.DateTimeField()),
                ('ended_at', models.DateTimeField()),
                ('total_time', models.TimeField()),
                ('inserted_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'last_refresh',
                'managed': False,
            },
        ),
    ]
