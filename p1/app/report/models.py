from django.db import models

# TODO: created_at and updated_at
# TODO: add a field to know status if was processed or not

# Create your models here.
class SheetSales(models.Model):
    id = models.AutoField(primary_key=True)
    chain_name = models.CharField(max_length=64)
    sub_chain_name = models.CharField(max_length=64)
    family_name = models.CharField(max_length=64)
    trademark_name = models.CharField(max_length=64)
    date = models.DateField()
    amount = models.FloatField(default=0)
    last_day = models.IntegerField(default=0)
    class Meta:
        db_table = 'sheet_sales' 


class SheetStock(models.Model):
    id = models.AutoField(primary_key=True)
    chain_name = models.CharField(max_length=64)
    sub_chain_name = models.CharField(max_length=64)
    family_name = models.CharField(max_length=64)
    trademark_name = models.CharField(max_length=64)
    date = models.DateField()
    stock_total = models.FloatField(default=0)
    daily_average = models.FloatField(default=0)

    class Meta:
        db_table = 'sheet_stock'


class SheetAlerts(models.Model):
    id = models.AutoField(primary_key=True)
    chain_name = models.CharField(max_length=64)
    sub_chain_name = models.CharField(max_length=64)
    family_name = models.CharField(max_length=64)
    trademark_name = models.CharField(max_length=64)
    date = models.DateField()
    sale_lost = models.FloatField(default=0)

    class Meta:
        db_table = 'sheet_alerts'
        

class B2BReport(models.Model):
    id = models.AutoField(primary_key=True)
    chain_name = models.CharField(max_length=64)
    sub_chain_name = models.CharField(max_length=64)
    family_name = models.CharField(max_length=64)
    trademark_name = models.CharField(max_length=64)
    sales_current_month = models.FloatField(default=0, null=True)
    sales_compare_month = models.FloatField(default=0, null=True) # puede no tener datos en el mes del año anterior
    sales_lost = models.FloatField(default=0, null=True) # puede no venir el dato en el csv de alertas
    sales_month_projection = models.FloatField(default=0, null=True) # puede no venir el dato en el csv de alertas
    stock = models.FloatField(default=0, null=True)
    daily_average = models.FloatField(default=0, null=True)

    class Meta:
        db_table = 'b2b_report'

    def __repr__(self) -> str:
        return f'[{self.chain_name}, {self.sub_chain_name}, {self.family_name}, {self.trademark_name}]'

