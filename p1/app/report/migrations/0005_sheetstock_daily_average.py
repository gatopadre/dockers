# Generated by Django 4.1.5 on 2023-01-30 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_b2breport_alter_sheetsales_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheetstock',
            name='daily_average',
            field=models.FloatField(default=0),
        ),
    ]
