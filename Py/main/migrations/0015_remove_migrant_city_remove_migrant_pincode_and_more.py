# Generated by Django 4.2.4 on 2023-10-02 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_remove_customuser_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='migrant',
            name='city',
        ),
        migrations.RemoveField(
            model_name='migrant',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='migrant',
            name='state',
        ),
        migrations.RemoveField(
            model_name='migrant',
            name='street_address',
        ),
    ]