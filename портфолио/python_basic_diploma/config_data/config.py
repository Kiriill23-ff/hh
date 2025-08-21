import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ('mortage','Расчёт ежемесечного платежа по ипотеки'),
    ('currency','Перевод из одной валюты в другую'),
     ('commodityprice','Цена на продуктовые фьючерсы и ценный метал'),
    ('cryptoprice','Цена на выбраннную криптовалюту'))
