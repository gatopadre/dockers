# Generated by Django 4.1.5 on 2023-01-24 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SheetAlerts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('chain_name', models.CharField(max_length=64)),
                ('sub_chain_name', models.CharField(max_length=64)),
                ('family_name', models.CharField(max_length=64)),
                ('trademark_name', models.CharField(max_length=64)),
                ('date', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'sheet_alerts',
            },
        ),
        migrations.CreateModel(
            name='SheetSales',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('chain_name', models.CharField(max_length=64)),
                ('sub_chain_name', models.CharField(max_length=64)),
                ('family_name', models.CharField(max_length=64)),
                ('trademark_name', models.CharField(max_length=64)),
                ('date', models.CharField(max_length=64)),
                ('amount', models.FloatField(default=0)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'sheet_sales',
            },
        ),
        migrations.CreateModel(
            name='SheetStock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('chain_name', models.CharField(max_length=64)),
                ('sub_chain_name', models.CharField(max_length=64)),
                ('family_name', models.CharField(max_length=64)),
                ('trademark_name', models.CharField(max_length=64)),
                ('date', models.DateField()),
                ('stock_total', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'sheet_stock',
            },
        ),
    ]