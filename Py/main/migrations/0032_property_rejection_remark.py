# Generated by Django 4.2.4 on 2024-01-31 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_property_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='rejection_remark',
            field=models.TextField(blank=True, null=True),
        ),
    ]