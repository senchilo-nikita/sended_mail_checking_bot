import requests
from read_mail import (check_kvadra_prices_forecast,
                       check_ses_united_green_forecast,
                       check_consum_sibintek_forecast,
                       check_generation_enel_forecast,
                       check_ses_lukoil_forecast)
import schedule
import time
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

recievers_dict = {
    'Никита Сенчило':'274176682',
    'Даниил Алмазкин':'156759640',
    'Алексей Цой':'931947053',
    'Андрей Огай':'371268489',
    'Александр Матыцин':'939471961'
}

def send_message_ses_united_green():
    """
    отправка сообщения с отчетом о рассылке прогноза выработки СЭС United Green
    """
    chat_id_list_ses = ['Никита Сенчило','Даниил Алмазкин','Александр Матыцин']
    message = check_ses_united_green_forecast()
    day_of_week = datetime.datetime.now().weekday()
    for chat_id in chat_id_list_ses:
        url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={recievers_dict[chat_id]}&text={message['message']}"
        if message['status'] == 'failed' and day_of_week not in [5,6]:
            requests.get(url)
        elif chat_id == 'Никита Сенчило':
            requests.get(url)

def send_message_kvadra():
    """
    отправка сообщения с отчетом о рассылке прогноза цены РСВ АО "Квадра"
    """
    chat_id_list_kvadra = ['Никита Сенчило','Даниил Алмазкин']
    message = check_kvadra_prices_forecast()
    for chat_id in chat_id_list_kvadra:
        url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={recievers_dict[chat_id]}&text={message['message']}"
        if message['status'] == 'failed':
            requests.get(url)
        elif chat_id == 'Никита Сенчило':
            requests.get(url)

def send_message_sibintek():
    """
    отправка сообщения с отчетом о рассылке прогноза потребления СибИнтек
    """
    chat_id_list = ['Никита Сенчило','Даниил Алмазкин','Александр Матыцин']
    message = check_consum_sibintek_forecast()
    for chat_id in chat_id_list:
        url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={recievers_dict[chat_id]}&text={message['message']}"
        if message['status'] == 'failed':
            requests.get(url)
        elif chat_id == 'Никита Сенчило':
            requests.get(url)

def send_message_enel():
    """
    отправка сообщения с отчетом о рассылке прогноза выработки ЭЭ Эл5-Энерго (Энел)
    """
    chat_id_list = ['Никита Сенчило','Даниил Алмазкин','Алексей Цой']
    message = check_generation_enel_forecast()
    for chat_id in chat_id_list:
        url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={recievers_dict[chat_id]}&text={message['message']}"
        if message['status'] == 'failed':
            requests.get(url)
        elif chat_id == 'Никита Сенчило':
            requests.get(url)

def send_message_lukoil_ses():
    """
    отправка сообщения с отчетом о рассылке прогноза выработки СЭС Лукойл
    """
    chat_id_list = ['Никита Сенчило','Даниил Алмазкин','Андрей Огай']
    message = check_ses_lukoil_forecast()
    for chat_id in chat_id_list:
        url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={recievers_dict[chat_id]}&text={message['message']}"
        if message['status'] == 'failed':
            requests.get(url)
        elif chat_id == 'Никита Сенчило':
            requests.get(url)

schedule.every().day.at("06:20", "Europe/Moscow").do(send_message_ses_united_green)
schedule.every().day.at("12:25", "Europe/Moscow").do(send_message_sibintek)
schedule.every().day.at("07:05", "Europe/Moscow").do(send_message_enel)
schedule.every().day.at("06:50", "Europe/Moscow").do(send_message_lukoil_ses)
schedule.every().friday.at("15:55", "Europe/Moscow").do(send_message_kvadra)

while True:
    schedule.run_pending()
    time.sleep(1)