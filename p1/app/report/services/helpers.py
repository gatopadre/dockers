import datetime
import requests
import pandas as pd

def get_date_from_today(days):
    """Get days from today"""
    today = datetime.date.today()
    days_from_today = today - datetime.timedelta(days=days)
    return days_from_today.strftime('%Y-%m-%d')


def get_days_from_date(num_days):
    """Get list with dates from today"""
    today = datetime.date.today()
    date_list = []
    for i in range(num_days):
        date = today - datetime.timedelta(days=i)
        date_list.append(date.strftime('%Y-%m-%d'))
    return date_list


def consume_api(method, url, data=None, headers=None, json=None):
    """Consume API"""
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=data, json=json)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=data, json=json)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers, data=data, json=json)
    else:
        return False

    if response.status_code == 200:
        return response.json()
    else:
        return False


def text_to_float(text):
    """Convert text to float"""
    try:
        return float(text.replace('.', '').replace(',', '.'))
    except Exception:
        return False


def text_to_int(text):
    """Convert text to int"""
    try:
        return int(text.replace('.', '').replace(',', '.'))
    except Exception:
        return False


def text_to_date(text):
    """Convert text to date"""
    try:
        return datetime.datetime.strptime(text, '%Y-%m-%d')
    except Exception:
        return False


def text_to_date_2(text):
    """Convert text to date"""
    try:
        date_object = datetime.datetime.strptime(text, "%d-%m-%Y")
        return date_object.strftime("%Y-%m-%d")
    except Exception:
        return False


def text_to_date_month_year(text):
    """Convert text to date"""
    try:
        return datetime.datetime.strptime(text, '%B %Y')
    except Exception:
        return False


def spanish_date_to_english(text):
    """Convert spanish date to english"""
    months_es_to_en = {
        "Enero": "January",
        "Febrero": "February",
        "Marzo": "March",
        "Abril": "April",
        "Mayo": "May",
        "Junio": "June",
        "Julio": "July",
        "Agosto": "August",
        "Septiembre": "September",
        "Octubre": "October",
        "Noviembre": "November",
        "Diciembre": "December"
    }
    month_es, year = text.split(" ")
    month_en = months_es_to_en[month_es]
    english_date_string = f"{month_en} {year}"
    return english_date_string


def casting_sale_date(text):
    text_date = spanish_date_to_english(text)
    return text_to_date_month_year(text_date)


def csv_to_df(file_path: str):
    """Save data from csv to database"""
    try:
        with open(file_path, 'r'):
            return pd.read_csv(file_path, encoding='latin-1', sep=';')
    except Exception as e:
        print(e)
        return False

    
def df_to_list(df: pd.DataFrame):
    """Convert df to list"""
    return df.to_dict('records')


def to_millions_format(number):
    if number is None or number == 0:
        return 0
    elif number >= 1000000000:
        return "{:.1f}B".format(number / 1000000000)
    elif number >= 1000000:
        return "{:.1f}M".format(number / 1000000)
    elif number < 1000000 and number >= 10000:
        return "{:.1f}K".format(number / 1000)
    elif number < 10000 and number > 0:
        return round(number, 1)
    elif number > -10000 and number < 0:
        return round(number, 1)
    elif number > -1000000 and number <= -10000:
        return "-{:.1f}K".format(abs(number) / 1000)
    elif number <= -1000000:
        return "-{:.1f}M".format(abs(number) / 1000000)
    elif number <= -1000000000:
        return "-{:.1f}B".format(abs(number) / 1000000000)
    else:
        return number
    

def to_millions_format(number):
    if number is None or number == 0:
        return 0
    elif number < 0:
        return "-{:,.2f}M".format(abs(number) / 1000000).replace(",", "*").replace(".", ",").replace("*", ".")
    else:
        return "{:,.2f}M".format(number / 1000000).replace(",", "*").replace(".", ",").replace("*", ".")

