# Generated by Django 4.2.4 on 2024-03-30 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_thread_chatmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('rejected', 'Rejected'), ('pending', 'Pending'), ('reserved', 'reserved'), ('checkedin', 'checkedin')], default='active', max_length=20),
        ),
    ]
