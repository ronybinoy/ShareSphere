# Generated by Django 4.2.4 on 2024-01-10 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_room_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='country_code',
            field=models.CharField(default='', max_length=5, null=True, verbose_name='country_code'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default='', max_length=15, null=True, verbose_name='phone'),
        ),
    ]
