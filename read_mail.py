from imbox import Imbox
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
LOGIN = os.getenv('EMAIL_LOGIN')
PASSWORD = os.getenv('EMAIL_PSWD')
EMAIL_SERVER = os.getenv('MAIL_SERVER')

def check_ses_united_green_forecast():
    """
    автоматическая проверка отправки прогноза выработки СЭС
    в United Green каждый ень в 6-15
    """
    today = datetime.datetime.now().date()
    str_today = today.strftime("%Y-%m-%d")
    login = LOGIN
    password = PASSWORD
    messages = []

    with Imbox(EMAIL_SERVER,
            username=login,
            password=password,
            ssl=True,
            ssl_context=None,
            starttls=False) as imbox:
        all_inbox_messages = imbox.messages(date__on=today)
        for uid, message in all_inbox_messages:
            if (message.sent_from[0]['email'] == 'AMatycin@nbiservice.ru' and
                message.subject.strip() == "Прогнозная выработка СЭС на трое суток вперед"):
                if len(message.attachments) > 0:
                    message_check = message.attachments[0]['filename'] == f'Forecast_NBI_{str_today}.xlsx'
                else:
                    message_check = 0
                messages.append(message_check)
    # хотя бы один файл за текуущие сутки должен содержать вложение с наименованием Forecast_NBI_{текущая дата}.xlsx
    messages_check = sum(messages)
    if messages_check >= 1:
        return {"status":'ok',
                "message":"Прогноз выработки СЭС United Green отправлен"}
    else:
        return {"status":'failed',
                "message":"Проверьте отправку прогноза выработки СЭС United Green!\nПрогноз может быть не доставлен."}

def check_kvadra_prices_forecast():
    """
    автоматическая проверка отправки прогноза цен РСВ
    в АО "Квадра" по пятницам в 15-45
    """
    today = datetime.datetime.now().date()
    str_start = (today + datetime.timedelta(days=1)).strftime("%d%m%Y")
    str_end = (today + datetime.timedelta(days=9)).strftime("%d%m%Y")

    login = LOGIN
    password = PASSWORD
    messages = []
    period = [str_start,str_end]
    with Imbox(EMAIL_SERVER,
            username=login,
            password=password,
            ssl=True,
            ssl_context=None,
            starttls=False) as imbox:
        all_inbox_messages = imbox.messages(date__on=today)
        for uid, message in all_inbox_messages:
            if (message.sent_from[0]['email'] == 'nsenchilo@nbiservice.ru'):
                message_period_start = (message.body['plain'][0].replace('.','').strip().split('с '[1]))[-3]
                message_period_end = (message.body['plain'][0].replace('.','').strip().split('с '[1]))[-1]
                message_period = [message_period_start,message_period_end]
                #  файл за текуущие сутки должен содержать вложение с наименованием kvadra.xlsx
                if "kvadra.xlsx" in message.raw_email:
                    message_check = 1
                else:
                    message_check = 0
                messages.append(message_period == period and message_check)
    # хотя бы один файл за сутки должен содержать файл kvadra.xlsx и указанный период прогноза
    messages_check = sum(messages)
    if messages_check >= 1:
        return {"status":'ok',
                "message":"Прогноз цены РСВ АО 'Квадра' отправлен"}
    else:
        return {"status":'failed',
                "message":"Проверьте отправку прогноза цены РСВ АО 'Квадра'!\nПрогноз может быть не доставлен."}
    