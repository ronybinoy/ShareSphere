# Generated by Django 4.2.4 on 2024-02-29 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_accbooking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accbooking',
            name='agreement',
        ),
    ]
