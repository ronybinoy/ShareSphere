# Generated by Django 4.2.4 on 2024-02-29 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_property_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accbooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('passport_number', models.CharField(max_length=20)),
                ('check_in_date', models.DateField()),
                ('num_adults', models.IntegerField()),
                ('special_requests', models.TextField(blank=True)),
                ('emergency_contact_name', models.CharField(max_length=100)),
                ('emergency_contact_relationship', models.CharField(max_length=100)),
                ('emergency_contact_phone', models.CharField(max_length=20)),
                ('agreement', models.BooleanField()),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
