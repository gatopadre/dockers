from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings
from django.db import connection
from django.core.mail import send_mail

from datetime import datetime
import requests
import os

from report.models import SheetSales, SheetStock, SheetAlerts
from report.services.helpers import (
    get_days_from_date, 
    consume_api, 
    text_to_float, 
    text_to_date, 
    casting_sale_date, 
    text_to_date_2, 
    to_millions_format, 
    df_to_list, 
    csv_to_df)


def send_report_by_email(request):
    receivers = ['szuniga@techk.cl', 'zunigasebastian@hotmail.com', 'renvergara@alumnos.uai.cl', 'rvergara@techk.cl']
    # receivers = ['rvergara@techk.cl', 'szuniga@techk.cl', 'ojerez@techk.cl', 'sgelmi@techk.cl', 'mabarca@techk.cl', 'jfernandez@techk.cl', 'jurrutia@techk.cl', 'cgarrido@icb.cl', 'pgallardo@icb.cl', 'drojic@icb.cl']
    # receivers = ['szuniga@techk.cl', 'zunigasebastian@hotmail.com', 'rvergara@techk.cl', 'sgelmi@techk.cl', 'ojerez@techk.cl']
    # receivers = ['szuniga@techk.cl', 'rvergara@techk.cl', 'zunigasebastian@hotmail.com', 'cgarrido@icb.cl', 'pgallardo@icb.cl', 'drojic@icb.cl']
    subject = 'Reporte Ventas B2B'
    template = 'template_embed_css.html'
    report_data_chains = get_data_by_chains()
    report_data_trademarks = get_data_by_trademarks()
    total_sales_current_month = 0
    total_sales_comparable_month = 0
    total_growth = 0
    total_variation = 0
    total_lost = 0
    total_projection = 0
    total_stock = 0
    total_stock_days = 0
    total_sale_daily = 0

    data_chains = []
    for item in report_data_chains:
        if item[1] == 'TOTAL':
            total_sales_current_month = total_sales_current_month + item[2]
            total_sales_comparable_month = total_sales_comparable_month + item[3]
            total_variation = total_variation + item[4]
            total_lost = total_lost + item[6]
            total_projection = total_projection + item[7]
            total_stock = total_stock + item[8]
            total_sale_daily = total_sale_daily + item[9]
        data_chains.append(
            [
                item[0], 
                item[1], 
                to_millions_format(item[2]), 
                to_millions_format(item[3]), 
                to_millions_format(item[4]), 
                item[5], 
                to_millions_format(item[6]), 
                to_millions_format(item[7]), 
                item[8], 
                item[9], 
                item[10]
            ])

    data_trademarks = []
    for item in report_data_trademarks:        
        data_trademarks.append(
            [
                item[0], 
                item[1], 
                to_millions_format(item[2]), 
                to_millions_format(item[3]), 
                to_millions_format(item[4]), 
                item[5], 
                to_millions_format(item[6]), 
                to_millions_format(item[7]), 
                item[8], 
                item[9], 
                item[10]
            ])

    total_stock_days = total_stock / total_sale_daily
    total_growth = total_variation / total_sales_comparable_month * 100
    total_sales_current_month = to_millions_format(total_sales_current_month)
    total_variation = to_millions_format(total_variation)
    total_projection = to_millions_format(total_projection)
    total_lost = to_millions_format(total_lost)

    # table
    data_last_updates = request_last_updates()

    content = {
            'report_chains': data_chains,
            'report_trademarks': data_trademarks,
            'now': datetime.now().strftime("%b %d, %Y"),
            'last_updates': data_last_updates,
            'total_sales_current_month': total_sales_current_month,
            'total_growth': round(total_growth, 1),
            'total_variation': total_variation,
            'total_lost': total_lost,
            'total_projection': total_projection,
            'total_stock': round(total_stock, 2),
            'total_stock_days': round(total_stock_days, 1),
            'averages_colors': {'green': 30, 'red': 20},
        }

    send_mail(
        subject,
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        receivers,
        fail_silently=True,
        html_message=render_to_string(template, content))

    return HttpResponse('Email sent')


def request_last_updates():
    """Get last updates from InstoreView API"""
    try:
        headers = {
            'Authorization': 'ISVToken 00f02b40087444649c23bf0bcab896d1',
            'Content-Type': 'application/json'
        }
        json_data = consume_api(
            'GET', 'https://api.instoreview.cl/api/v2/categories/', headers=headers)
        return json_data['lastChainUpdates']['chains']
    except Exception as e:
        print(e)
        return False


def request_sales_csv_url(years: list):
    """Get sales csv from InstoreView API"""
    headers = {
        'Authorization': 'ISVToken 00f02b40087444649c23bf0bcab896d1',
        'Content-Type': 'application/json'
    }

    json = {
        "view_type": "mes_curso",
        "dates": years,
        "views": [
            "PVP s/IVA"
        ],
        "compress": "false",
        "hierarchy": {
            "Cadena": [],
            "Sub Cadena": [],
            "Familia ICB": [],
            "Marca ICB": []
        }
    }
    return consume_api('POST', 'https://api.instoreview.cl/api/v2/download-zone/sales/', headers=headers, json=json)


def request_alerts_csv_url():
    """Get alerts csv from InstoreView API"""
    headers = {
        'Authorization': 'ISVToken 00f02b40087444649c23bf0bcab896d1',
        'Content-Type': 'application/json'
    }

    json = {
        "dates": get_days_from_date(15),
        "views": [
            "PVP s/IVA"
        ],
        "compress": "false",
        "hierarchy": {
            "Cadena": [],
            "Sub Cadena": [],
            "Familia ICB": [],
            "Marca ICB": []
        }
    }

    return consume_api('POST', 'https://api.instoreview.cl/api/v2/download-zone/alerts/', headers=headers, json=json)


def request_stock_csv_url():
    """Get stock csv from InstoreView API"""
    headers = {
        'Authorization': 'ISVToken 00f02b40087444649c23bf0bcab896d1',
        'Content-Type': 'application/json'
    }

    json = {
        "views": [
            "Unidades"
        ],
        "last_category_update": "true",
        "compress": "false",
        "hierarchy": {
            "Cadena": [],
            "Sub Cadena": [],
            "Familia ICB": [],
            "Marca ICB": []
        }
    }

    return consume_api('POST', 'https://api.instoreview.cl/api/v2/download-zone/stock/', headers=headers, json=json)


def download_file(file_url: str, file_name: str):
    """Download file from url"""
    try:
        response = requests.get(file_url, stream=True)
        with open(f'{settings.DOWNLOAD_DIR}/{file_name}', 'wb') as file:
            file.write(response.content)
        return f'{settings.DOWNLOAD_DIR}/{file_name}'
    except Exception as e:
        print(e)
        return False


def delete_file(file_path: str):
    """Delete file from download directory"""
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        print(e)
        return False


def get_files_to_local():
    """Download files from InstoreView API"""
    sales = request_sales_csv_url()
    alerts = request_alerts_csv_url()
    stock = request_stock_csv_url()

    if sales['status'] == 200 and alerts['status'] == 200 and stock['status'] == 200:
        sales_file = download_file(sales['data']['url'], 'sales.csv')
        alerts_file = download_file(alerts['data']['url'], 'alerts.csv')
        stock_file = download_file(stock['data']['url'], 'stock.csv')
        return sales_file and alerts_file and stock_file
    return False


def saving_sales_to_db(data: dict):
    """Save sales data to database"""
    try:
        last_updates = request_last_updates()
        # print(last_updates)        
        for item in data:
            day = None
            for last_day in last_updates:                
                if last_day['name'] == item['Cadena']:
                    day = last_day['lastUpdate'][:2]
                    break
            obj = SheetSales(
                chain_name=item['Cadena'],
                sub_chain_name=item['Sub Cadena'],
                family_name=item['Familia ICB'],
                trademark_name=item['Marca ICB'],
                date=casting_sale_date(item['Mes en curso']),  # se tiene que castear la fecha para que sea compatible con el modelo
                amount=text_to_float(item['PVP s/IVA']),
                last_day=day
            )
            obj.save()
            del obj
        return True
    except Exception as e:
        print(e)
        return False


def saving_stock_to_db(data: dict):
    """Save stock data to database"""
    try:
        for item in data:
            obj = SheetStock(
                chain_name=item['Cadena'],
                sub_chain_name=item['Sub Cadena'],
                family_name=item['Familia ICB'],
                trademark_name=item['Marca ICB'],
                date=text_to_date_2(item['Fechas']),
                stock_total=text_to_float(item['Stock Total en Unidades']),
                daily_average=text_to_float(item['Promedio Diario Ventas en Unidades']),
            )
            obj.save()
            del obj
        return True
    except Exception as e:
        print(e)
        return False


def saving_alerts_to_db(data: dict):
    """Save alerts data to database"""
    try:
        for item in data:
            obj = SheetAlerts(
                chain_name=item['Cadena'],
                sub_chain_name=item['Sub Cadena'],
                family_name=item['Familia ICB'],
                trademark_name=item['Marca ICB'],
                date=text_to_date(item['Fechas']),
                sale_lost=text_to_float(item['Venta Quiebre en PVP s/IVA']),
            )
            obj.save()
            del obj
        return True
    except Exception as e:
        print(e)
        return False


def get_data_by_chains():
    """Get data from database"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            select chain_name, 
            sub_chain_name, 
            sum(sales_current_month) as sales_current_month,
            sum(sales_compare_month) as sales_compare_month,
            sum(sales_current_month) - sum(sales_compare_month) as sales_variation,
            case
                when sum(sales_compare_month) = 0 then 0
                when sum(sales_compare_month) > 0 then (sum(sales_current_month) - sum(sales_compare_month)) / sum(sales_compare_month) * 100
                else 0
            end as sales_growth,
            sum(sales_lost) as sales_lost,
            sum(sales_month_projection) as sales_month_projection,
            sum(stock) as stock,
            sum(daily_average) as daily_average,
            case 
                when sum(daily_average) = 0 then 0  
                when sum(daily_average) > 0 then sum(stock) / sum(daily_average)
                else 0 
            end as stock_days,
            '0'as flag 
            from b2b_report bbr 
            group by chain_name, sub_chain_name
            union select chain_name,
            'TOTAL' as sub_chain_name, 
            sum(sales_current_month) as sales_current_month,
            sum(sales_compare_month) as sales_compare_month,
            sum(sales_current_month) - sum(sales_compare_month) as sales_variation,
            case
                when sum(sales_compare_month) = 0 then 0
                when sum(sales_compare_month) > 0 then (sum(sales_current_month) - sum(sales_compare_month)) / sum(sales_compare_month) * 100
                else 0
            end as sales_growth,
            sum(sales_lost) as sales_lost,
            sum(sales_month_projection) as sales_month_projection,
            sum(stock) as stock,
            sum(daily_average) as daily_average,
            case 
                when sum(daily_average) = 0 then 0  
                when sum(daily_average) > 0 then sum(stock) / sum(daily_average)
                else 0 
            end as stock_days,
            '1'as flag 
            from b2b_report bbr 
            group by chain_name
            order by chain_name asc, flag asc, sub_chain_name asc;""")
            return list(cursor.fetchall())
    except Exception as e:
        print(e)
        return False


def get_data_by_trademarks():
    try:
        with connection.cursor() as cursor:
            cursor.execute("""select trademark_name, family_name,
                sum(sales_current_month) as sales_current_month,
                sum(sales_compare_month) as sales_compare_month,
                sum(sales_current_month) - sum(sales_compare_month) as sales_variation,
                case
                    when sum(sales_compare_month) = 0 then 0
                    when sum(sales_compare_month) > 0 then (sum(sales_current_month) - sum(sales_compare_month)) / sum(sales_compare_month) * 100
                    else 0
                end as sales_growth,
                sum(sales_lost) as sales_lost,
                sum(sales_month_projection) as sales_month_projection,
                sum(stock) as stock,
                sum(daily_average) as daily_average,
                case 
                    when sum(daily_average) = 0 then 0  
                    when sum(daily_average) > 0 then sum(stock) / sum(daily_average)
                    else 0 
                end as stock_days,
                '0'as flag 
                from b2b_report bbr 
                group by trademark_name, family_name 
                union
                select  trademark_name,'TOTAL' as family_name,
                sum(sales_current_month) as sales_current_month,
                sum(sales_compare_month) as sales_compare_month,
                sum(sales_current_month) - sum(sales_compare_month) as sales_variation,
                case
                    when sum(sales_compare_month) = 0 then 0
                    when sum(sales_compare_month) > 0 then (sum(sales_current_month) - sum(sales_compare_month)) / sum(sales_compare_month) * 100
                    else 0
                end as sales_growth,
                sum(sales_lost) as sales_lost,
                sum(sales_month_projection) as sales_month_projection,
                sum(stock) as stock,
                sum(daily_average) as daily_average,
                case 
                    when sum(daily_average) = 0 then 0  
                    when sum(daily_average) > 0 then sum(stock) / sum(daily_average)
                    else 0 
                end as stock_days,
                '1'as flag 
                from b2b_report bbr 
                group by trademark_name
                order by trademark_name, flag asc;""")
            return list(cursor.fetchall())
    except Exception as e:
        print(e)
        return False


def get_totals_by_chain_subchain():
    try:
        with connection.cursor() as cursor:
            cursor.execute("""select '' as id,chain_name, 
                sub_chain_name, 
                'TOTAL' as family_name, 
                'TOTAL' as trademark_name,
                sum(sales_current_month) as sales_current_month,
                sum(sales_compare_month) as sales_compare_month,
                sum(sales_variation) as sales_variation,
                sum(sales_growth) as sales_growth,
                sum(sales_lost) as sales_lost,
                sum(sales_month_projection) as sales_month_projection,
                sum(stock) as stock,
                sum(daily_average) as daily_average,
                sum(stock_days) as stock_days
                from b2b_report bbr 
                group by chain_name, sub_chain_name
                order by chain_name, sub_chain_name;""")
            return list(cursor.fetchall())
    except Exception as e:
        print(e)
        return False


def delete_sales():
    try:
        with connection.cursor() as cursor:
            cursor.execute("""TRUNCATE sheet_sales RESTART IDENTITY;""")
            return True
    except Exception as e:
        print(e)
        return False


def delete_b2b():
    try:
        with connection.cursor() as cursor:
            cursor.execute("""TRUNCATE b2b_report RESTART IDENTITY;""")
            return True
    except Exception as e:
        print(e)
        return False


def delete_alerts():
    try:
        with connection.cursor() as cursor:
            cursor.execute("""TRUNCATE sheet_alerts RESTART IDENTITY;""")
            return True
    except Exception as e:
        print(e)
        return False


def delete_stock():
    try:
        with connection.cursor() as cursor:
            cursor.execute("""TRUNCATE sheet_stock RESTART IDENTITY;""")
            return True
    except Exception as e:
        print(e)
        return False


def get_and_save_sales():
    years = ['2022', '2023']
    delete_sales()
    url = request_sales_csv_url(years)  # obtiene la url del archivo en amazon
    sales_file = download_file(url['download_url'], 'sales.csv')  # descarga el archivo y lo pone en la carpeta downloads
    df_sales = csv_to_df(sales_file)  # datos del csv a dataframe
    delete_file(sales_file)  # borra el archivo de la carpeta downloads
    lista_sales = df_to_list(df_sales)  # dataframe a lista
    saving_sales_to_db(lista_sales)  # guarda los datos en la base de datos
    return True


def get_and_save_alerts():
    delete_alerts()
    url = request_alerts_csv_url()  # obtiene la url del archivo en amazon
    alerts_file = download_file(url['download_url'], 'alerts.csv')  # descarga el archivo y lo pone en la carpeta downloads
    df_alerts = csv_to_df(alerts_file)  # datos del csv a dataframe
    delete_file(alerts_file)  # borra el archivo de la carpeta downloads
    lista_alerts = df_to_list(df_alerts)  # dataframe a lista
    saving_alerts_to_db(lista_alerts)  # guarda los datos en la base de datos
    return True


def get_and_save_stocks():
    delete_stock()
    url = request_stock_csv_url()  # obtiene la url del archivo en amazon
    stock_file = download_file(url['download_url'], 'stock.csv')  # descarga el archivo y lo pone en la carpeta downloads
    df_stock = csv_to_df(stock_file)  # datos del csv a dataframe
    delete_file(stock_file)  # borra el archivo de la carpeta downloads
    lista_stock = df_to_list(df_stock)  # dataframe a lista
    saving_stock_to_db(lista_stock)  # guarda los datos en la base de datos
    return True


def show_report(request):
    template = 'index.html'
    report_data_chains = get_data_by_chains()
    report_data_trademarks = get_data_by_trademarks()
    total_sales_current_month = 0
    total_sales_comparable_month = 0
    total_growth = 0
    total_variation = 0
    total_lost = 0
    total_projection = 0
    total_stock = 0
    total_stock_days = 0
    total_sale_daily = 0

    # Suma los totales
    data_chains = []
    for item in report_data_chains:
        if item[1] == 'TOTAL':
            # obteniendo totales
            total_sales_current_month = total_sales_current_month + item[2]
            total_sales_comparable_month = total_sales_comparable_month + item[3]
            total_variation = total_variation + item[4]
            total_lost = total_lost + item[6]
            total_projection = total_projection + item[7]
            total_stock = total_stock + item[8]
            total_sale_daily = total_sale_daily + item[9]   
        # casteando a millones
        data_chains.append(
            [
                item[0], 
                item[1], 
                to_millions_format(item[2]), 
                to_millions_format(item[3]), 
                to_millions_format(item[4]), 
                item[5], 
                to_millions_format(item[6]), 
                to_millions_format(item[7]), 
                item[8], 
                item[9], 
                item[10]
            ])

    # casteando a millones
    data_trademarks = []
    for item in report_data_trademarks:        
        data_trademarks.append(
            [
                item[0], 
                item[1], 
                to_millions_format(item[2]), 
                to_millions_format(item[3]), 
                to_millions_format(item[4]), 
                item[5], 
                to_millions_format(item[6]), 
                to_millions_format(item[7]), 
                item[8], 
                item[9], 
                item[10]
            ])

    # Totales
    total_stock_days = total_stock / total_sale_daily
    total_growth = total_variation / total_sales_comparable_month * 100
    total_sales_current_month = to_millions_format(total_sales_current_month)
    total_variation = to_millions_format(total_variation)
    total_projection = to_millions_format(total_projection)
    total_lost = to_millions_format(total_lost)

    # tabla de ultimas actualizaciones
    data_last_updates = request_last_updates()

    return render(
        request,
        template,
        {
            'report_chains': data_chains,
            'report_trademarks': data_trademarks,
            'now': datetime.now().strftime("%b %d, %Y"),
            'last_updates': data_last_updates,
            'total_sales_current_month': total_sales_current_month,
            'total_growth': round(total_growth, 1),
            'total_variation': total_variation,
            'total_lost': total_lost,
            'total_projection': total_projection,
            'total_stock': round(total_stock, 2),
            'total_stock_days': round(total_stock_days, 1),
            'averages_colors': {'green': 30, 'red': 20},
        }
    )


def get_data(request):
    get_and_save_alerts()
    get_and_save_sales()
    get_and_save_stocks()
    return HttpResponse('Data saved in sheets tables')


def process_data(request):
    try:
        delete_b2b()
        with connection.cursor() as cursor:
            cursor.execute("""insert into b2b_report (chain_name, sub_chain_name, family_name, trademark_name, sales_current_month, sales_compare_month, sales_lost, sales_month_projection, stock, daily_average)
            select universo.chain_name, 
            universo.sub_chain_name, 
            universo.family_name, 
            universo.trademark_name,
            universo.sales_current_month,
            universo.sales_compare_month,
            universo.sales_lost,
            universo.sales_month_projection,
            t_stock.stock_total as stock, 
            t_stock.daily_average
            from
            (Select sales.chain_name, 
                sales.sub_chain_name, 
                sales.family_name, 
                sales.trademark_name,
                sum(sales.sales_compare_month) sales_compare_month,
                sum(sales.sales_current_month) sales_current_month,
                (select sum(sale_lost)
                from sheet_alerts sa 
                where sales.chain_name = sa.chain_name 
                    and sales.sub_chain_name = sa.sub_chain_name 
                    and sales.family_name = sa.family_name
                    and sales.trademark_name = sa.trademark_name
                group by sales.chain_name, sales.sub_chain_name, sales.family_name, sales.trademark_name) as sales_lost,
                sum(sales.sales_current_month) / sales.last_day * extract(day from(date_trunc('month', current_date) + interval '1 month') - date_trunc('month', current_date)) as sales_month_projection
            From(
                select ss.chain_name, 
                ss.sub_chain_name, 
                ss.family_name, 
                ss.trademark_name,
                (CASE when 
                date_part('year', ss."date") >= date_part('year', current_date) then ss.amount
                else 0 end) as sales_current_month,
                (CASE when date_part('year', ss."date") < date_part('year', current_date) then ss.amount
                else 0 end) as sales_compare_month,
                ss.last_day
                from sheet_sales ss) as sales
            where sales.sub_chain_name <> 'OK Market'
            Group by sales.chain_name, 
                sales.sub_chain_name, 
                sales.family_name, 
                sales.trademark_name,
                sales.last_day
            order by sales.chain_name, 
                sales.sub_chain_name, 
                sales.family_name, 
                sales.trademark_name) as universo
            left join sheet_stock t_stock 
                on universo.chain_name = t_stock.chain_name 
                    and universo.sub_chain_name = t_stock.sub_chain_name 
                    and universo.family_name = t_stock.family_name
                    and universo.trademark_name = t_stock.trademark_name;""")
            return HttpResponse('Data saved in b2b_report table')
    except Exception as e:
        print(e)
        return False


def test(request):
    get_data(request)
    process_data(request)
    send_report_by_email(request)
    return HttpResponse('Process finished')
