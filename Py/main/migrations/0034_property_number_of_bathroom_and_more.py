# Generated by Django 4.2.4 on 2024-02-06 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_property_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='number_of_bathroom',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], default=0),
        ),
        migrations.AddField(
            model_name='property',
            name='total_squarefeet',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
