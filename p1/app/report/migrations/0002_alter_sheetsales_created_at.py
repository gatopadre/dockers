# Generated by Django 4.1.5 on 2023-01-25 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheetsales',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
