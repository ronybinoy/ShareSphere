# Generated by Django 4.2.4 on 2023-10-02 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_migrant_city_remove_migrant_pincode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_application',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]