# Generated by Django 5.1.4 on 2025-04-23 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('size', models.CharField(max_length=20)),
                ('format', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'tb_network_forensics',
            },
        ),
    ]
