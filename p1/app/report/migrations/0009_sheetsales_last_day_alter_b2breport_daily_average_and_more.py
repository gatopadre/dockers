# Generated by Django 4.1.5 on 2023-02-20 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_alter_b2breport_sales_month_projection'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheetsales',
            name='last_day',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='b2breport',
            name='daily_average',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='b2breport',
            name='sales_current_month',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='b2breport',
            name='stock',
            field=models.FloatField(default=0, null=True),
        ),
    ]