# Generated by Django 4.1.5 on 2023-02-13 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0007_alter_b2breport_sales_compare_month_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='b2breport',
            name='sales_month_projection',
            field=models.FloatField(default=0, null=True),
        ),
    ]
