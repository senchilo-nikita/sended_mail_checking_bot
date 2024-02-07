import requests
from read_mail import check_kvadra_prices_forecast, check_ses_united_green_forecast
import schedule
import time
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

def send_message_ses():
    """
    отправка сообщения с отчетом о рассылке прогноза выработки СЭС United Green
    """
    chat_id_list_ses = ['274176682','939471961']
    message = check_ses_united_green_forecast()
    for chat_id in chat_id_list_ses:
        url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={message['message']}"
        if message['status'] == 'failed':
            requests.get(url)

def send_message_kvadra():
    """
    отправка сообщения с отчетом о рассылке прогноза цены РСВ АО "Квадра"
    """
    chat_id_list_kvadra = ['274176682']
    message = check_kvadra_prices_forecast()
    for chat_id in chat_id_list_kvadra:
        url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={message['message']}"
        if message['status'] == 'failed':
            requests.get(url)


schedule.every().day.at("06:20", "Europe/Moscow").do(send_message_ses)
schedule.every().friday.at("15:55").do(send_message_kvadra)

while True:
    schedule.run_pending()
    time.sleep(1)