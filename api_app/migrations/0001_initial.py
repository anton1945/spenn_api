# Generated by Django 5.0.7 on 2024-07-23 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.CharField(max_length=64)),
                ('response_id', models.CharField(max_length=64)),
                ('status', models.CharField(max_length=20)),
                ('external_reference', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('message', models.CharField(max_length=255)),
                ('external_reference', models.CharField(max_length=64)),
                ('request_id', models.CharField(blank=True, max_length=64, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
