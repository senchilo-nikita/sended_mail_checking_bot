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
                message.subject.strip() == "НБИ. Прогноз выработки СЭС United Green на трое суток вперед"):
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
        for i in range(len(all_inbox_messages)):
            try:
                message = all_inbox_messages[i][1]
                if (message.sent_from[0]['email'] == "nsenchilo@nbiservice.ru"):
                    message_period_start = (message.body['plain'][0].replace('.','').strip().split('с '[1]))[-3]
                    message_period_end = (message.body['plain'][0].replace('.','').strip().split('с '[1]))[-1]
                    message_period = [message_period_start,message_period_end]
                    #  файл за текуущие сутки должен содержать вложение с наименованием kvadra.xlsx
                    if "kvadra.xlsx" in message.raw_email:
                        message_check = 1
                    else:
                        message_check = 0
                    messages.append(message_period == period and message_check)
            except Exception as e:
                print("Error: ",e)
    # хотя бы один файл за сутки должен содержать файл kvadra.xlsx и указанный период прогноза
    messages_check = sum(messages)
    if messages_check >= 1:
        return {"status":'ok',
                "message":"Прогноз цены РСВ АО 'Квадра' отправлен"}
    else:
        return {"status":'failed',
                "message":"Проверьте отправку прогноза цены РСВ АО 'Квадра'!\nПрогноз может быть не доставлен."}
    

def check_consum_sibintek_forecast():
    """
    автоматическая проверка отправки прогноза потребления 
    СибИнтек каждый день в 12-45
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
        for i in range(len(all_inbox_messages)):
            # try:
            message = all_inbox_messages[i][1]
            print(message.subject)
            if (message.sent_from[0]['email'] == 'AMatycin@nbiservice.ru' and
                message.subject.strip() == "НБИ. Прогноз генерации и потребления УВНГ на двое суток вперед"):
                if len(message.attachments) > 0:
                    message_check = 1
                else:
                    message_check = 0
                messages.append(message_check)
            # except Exception as e:
            #     print("Error: ",e)
    # хотя бы один файл за текуущие сутки должен содержать вложение с наименованием Forecast_NBI_{текущая дата}.xlsx
    messages_check = sum(messages)
    if messages_check >= 1:
        return {"status":'ok',
                "message":"Прогноз потребления СибИнтек отправлен"}
    else:
        return {"status":'failed',
                "message":"Проверьте отправку прогноза потребления СибИнтек!\nПрогноз может быть не доставлен."}
    
def check_generation_enel_forecast():
    """
    автоматическая проверка отправки прогноза генерации
    Эл5-Энерго (Энел) каждый день в 7:03
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
        for i in range(len(all_inbox_messages)):
            try:
                message = all_inbox_messages[i][1]
                s = message.subject.strip()
                result_string = ' '.join(s.split(' ')[:-2])
                if (message.sent_from[0]['email'] == 'dfs@nbiservice.ru' and
                    result_string == 'НБИ. Прогноз выработки ЭЭ Эл5-Энерго'):
                    if len(message.attachments) > 0:
                        message_check = message.attachments[0]['filename'] == 'forecast.xlsx'
                    else:
                        message_check = 0
                    messages.append(message_check)
            except Exception as e:
                print("Error: ",e)
    # хотя бы один файл за текуущие сутки должен содержать вложение с наименованием Forecast_NBI_{текущая дата}.xlsx
    messages_check = sum(messages)
    if messages_check >= 1:
        return {"status":'ok',
                "message":"Прогноз генерации Энел отправлен"}
    else:
        return {"status":'failed',
                "message":"Проверьте отправку прогноза генерации Энел!\nПрогноз может быть не доставлен."}
    

def check_ses_lukoil_forecast():
    """
    автоматическая проверка отправки прогноза генерации
    СЭС ЛукОйл каждый день в 6-50
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
        for i in range(len(all_inbox_messages)):
            try:
                message = all_inbox_messages[i][1]
                # print(message.subject, message.sent_from[0]['email'])
                s = message.subject.strip()
                result_string = ' '.join(s.split(' ')[:-4])
                if (message.sent_from[0]['email'] == 'solar1_forecast@nbiservice.ru' and
                    result_string == 'НБИ. Прогноз генерации СЭС Лукойл'):
                    if len(message.attachments) > 0:
                        message_check = 1
                    else:
                        message_check = 0
                    messages.append(message_check)
            except Exception as e:
                print("Error: ",e)
    # хотя бы один файл за текуущие сутки должен содержать вложение с наименованием Forecast_NBI_{текущая дата}.xlsx
    messages_check = sum(messages)
    if messages_check >= 1:
        return {"status":'ok',
                "message":"Прогноз генерации СЭС Лукойл отправлен"}
    else:
        return {"status":'failed',
                "message":"Проверьте отправку прогноза генерации СЭС Лукойл!\nПрогноз может быть не доставлен."}

print(check_consum_sibintek_forecast())