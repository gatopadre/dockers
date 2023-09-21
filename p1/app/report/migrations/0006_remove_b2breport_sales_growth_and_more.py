# Generated by Django 4.1.5 on 2023-02-13 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_sheetstock_daily_average'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='b2breport',
            name='sales_growth',
        ),
        migrations.RemoveField(
            model_name='b2breport',
            name='sales_variation',
        ),
        migrations.RemoveField(
            model_name='b2breport',
            name='stock_days',
        ),
        migrations.AddField(
            model_name='sheetalerts',
            name='sale_lost',
            field=models.FloatField(default=0),
        ),
    ]
