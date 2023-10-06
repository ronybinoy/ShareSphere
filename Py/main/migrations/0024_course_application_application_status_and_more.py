# Generated by Django 4.2.4 on 2023-10-05 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_remove_course_application_application_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_application',
            name='application_status',
            field=models.CharField(choices=[('applied', 'Applied'), ('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='applied', max_length=10),
        ),
        migrations.AlterField(
            model_name='course_application',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
