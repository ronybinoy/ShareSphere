# Generated by Django 4.2.4 on 2023-10-02 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_course_application_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course_application',
            name='status',
        ),
    ]
