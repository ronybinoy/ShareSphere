# Generated by Django 4.2.4 on 2023-10-02 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_remove_course_application_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_application',
            name='application_status',
            field=models.BooleanField(default=False),
        ),
    ]
