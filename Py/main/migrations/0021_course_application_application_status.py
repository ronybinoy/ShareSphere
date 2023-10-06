# Generated by Django 4.2.4 on 2023-10-05 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_rename_application_status_course_application_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_application',
            name='application_status',
            field=models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
