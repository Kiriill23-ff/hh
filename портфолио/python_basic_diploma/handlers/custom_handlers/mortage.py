from loader import bot
from states.mortage import InformationMortage
from telebot.types import Message
import requests
from config_data import config
from telebot import types
import json

@bot.message_handler(commands=["mortage"])
def servey(message:Message) -> None:
    bot.set_state(message.from_user.id, InformationMortage.cost, message.chat.id)
    bot.send_message(message.from_user.id,text=f'Здравствуйте {message.from_user.username}, '
                                          f'ввидити стоимость желья, которое хотели бы приобрести:')

    @bot.message_handler(state=InformationMortage.cost)
    def get_procent(message: Message) -> None:
        if message.text.isdigit():
            bot.send_message(message.from_user.id, text=f'Ввидите пожалуйста одобренную вам процентную ставку.'
                                                        f'Если она является десятичным числом - запишите пожалуйста через точку:')
            bot.set_state(message.from_user.id, InformationMortage.procent, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['cost'] = message.text
        else:
            bot.send_message(message.from_user.id, f'Стоиомость желья должна быть цифрой:')

    @bot.message_handler(state=InformationMortage.procent)
    def get_years(message: Message) -> None:
        verefication = message.text.replace('.', '')
        if verefication.isdigit():
            bot.send_message(message.from_user.id, f'Введите на сколько лет хотите взять ипотеку:')
            bot.set_state(message.from_user.id, InformationMortage.years, message.chat.id)

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['procent'] = message.text

        else:
            bot.send_message(message.from_user.id, f'Процентная ставка может быть только числом:')

    @bot.message_handler(state=InformationMortage.years)
    def get_years(message: Message) -> None:
        if message.text.isdigit():
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['years'] = message.text
            button_1 = types.InlineKeyboardMarkup(row_width=1)
            button_2 = types.InlineKeyboardButton('Получить результат', callback_data='truth_1')
            button_1.add(button_2)
            text = (f'Полученная информация:\n'
                    f'Стоимость желья:{data['cost']}\n'
                    f'Процентная ставка:{data['procent']}\n'
                    f'Срок ипотеки:{data['years']}')
            bot.send_message(message.from_user.id, text, reply_markup=button_1)

            @bot.callback_query_handler(func=lambda call: True)
            def callback(call):
                if call.data == 'truth_1':
                    api_url = ('https://api.api-ninjas.com/v1/mortgagecalculator?loan_amount={}'
                               '&interest_rate={}&duration_years={}').format(data['cost'], data['procent'],
                                                                             data['years'])
                    response = requests.get(api_url, headers={'X-Api-Key': config.RAPID_API_KEY})
                    for i in json.loads(response.text):
                        if i == 'monthly_payment':
                           result = f'Ежемесячный платёж составит:{json.loads(response.text)[i]['total']}'
                           bot.send_message(message.from_user.id,result)
        else:
            bot.send_message(message.from_user.id, f'Срок ипотеки должен быть числом:')









