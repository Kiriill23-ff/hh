from loader import bot
from states.currency import InformationCurrency
from telebot.types import Message
import requests
from config_data import config
from telebot import types
import json

spisok_currency_user = ('\n1.HKD	Гонконгский доллар - Китайский юань\n2.CHF - Швейцарский франк\n3.AUD - Австралийский доллар\n4.PLN - Польский злоты\n'
                        '5.TRY - Новая Турецкая Лира\n6.GBP - Британский фунт\n'
                        '7.NZD - Новозеландский доллар\n8.KRW- Южнокорейская вона\n'
                        '9.DKK - Датская крона\n10.HKD	Гонконгский доллар\n')
spisok_currency ={1:'HKD',2:'CHF',3:'AUD',4:'PLN',5:'TRY',6:'GBP',7:'NZD',8:'KRW',9:'DKK',10:'HKD'}

@bot.message_handler(commands=["currency"])
def servey(message:Message) -> None:
    bot.set_state(message.from_user.id, InformationCurrency.current_currency, message.chat.id)
    bot.send_message(message.from_user.id,text=f'Здравствуйте {message.from_user.username}.Список валют:\n{spisok_currency_user} '
                                          f'ввидите цифру стоящую около валюту которую хотите поменять:')

    @bot.message_handler(state=InformationCurrency.current_currency)
    def get_procent(message: Message) -> None:
        if message.text.isdigit() and (int(message.text) < 11):
            result = int(message.text)
            bot.send_message(message.from_user.id, text=f'Ввидите пожалуйста цифру, валюты в которую вы хотите перевести:')
            bot.set_state(message.from_user.id,InformationCurrency.get_currency, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['current_currency'] = spisok_currency[result]
        else:
            if not message.text.isdigit():
                bot.send_message(message.from_user.id, f'Обозначение выбранной вами валюты должна быть цифрой.Повторите ввод:')
            if int(message.text) > 10:
                bot.send_message(message.from_user.id, f'Введённое значение больше предоставляемого количества валют.Повторите ввод:')

    @bot.message_handler(state=InformationCurrency.get_currency)
    def get_procent(message: Message) -> None:
        if message.text.isdigit() and (int(message.text) < 11):
            result = int(message.text)
            bot.send_message(message.from_user.id,
                             text=f'Ввидите пожалуйста cумму денег которую нужно преобразовать:')
            bot.set_state(message.from_user.id, InformationCurrency.summ_currency, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['get_currency'] = spisok_currency[result]
        else:
            if not message.text.isdigit():
                bot.send_message(message.from_user.id,
                                 f'Обозначение выбранной вами валюты должна быть цифрой.Повторите ввод:')
            if int(message.text) > 10:
                bot.send_message(message.from_user.id,
                                 f'Введённое значение больше предоставляемого количества валют.Повторите ввод:')

    @bot.message_handler(state=InformationCurrency.summ_currency)
    def get_procent(message: Message) -> None:
        if message.text.isdigit():
            result = int(message.text)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['summ_currency'] = result
                text = (f'Полученная информация:\n'
                        f'Текущая валюта:{data['current_currency']}\n'
                        f'Какую хотите получить:{data['get_currency']}\n'
                        f'Сумма перевода:{data['summ_currency']}')
                bot.send_message(message.from_user.id, text)
                api_url = ('https://api.api-ninjas.com/v1/convertcurrency?have={}&want={}&amount={}').format(data['current_currency'],
                                                                                                                     data['get_currency'],data['summ_currency'])
                response = requests.get(api_url, headers={'X-Api-Key': config.RAPID_API_KEY})
                for i in json.loads(response.text):
                    if i == "new_amount":
                        result = f'Результат:{json.loads(response.text)['new_amount']} {data['get_currency']}'
                        bot.send_message(message.from_user.id,result)
        else:
            bot.send_message(message.from_user.id,f'Сумма должна быть цифрами:')





