from loader import bot
from states.cryptoprice import InformationCrypto
from telebot.types import Message
import requests
from config_data import config
from telebot import types
import json

spisok_coomod_user = (f'1.BTCUSD\n2.1INCHUSD\n3.CELOUSDT\n4.DARUSDT\n5.ETHDAI\n6.ILVUSD')
spisok_coomod_work = {1:'BTCUSD',2:'1INCHUSD',3:'CELOUSDT',4:'DARUSDT',
                      5:'ETHDAI',6:'ILVUSD'}

@bot.message_handler(commands=["cryptoprice"])
def servey(message:Message) -> None:
    bot.set_state(message.from_user.id, InformationCrypto.name_crypto, message.chat.id)
    bot.send_message(message.from_user.id,text=f'Здравствуйте {message.from_user.username}.Список криптоволют:'
                                               f':\n{spisok_coomod_user}\n'
                                          f'Ввидите цифру стоящую около интересающей вас криптоволюте:')

    @bot.message_handler(state=InformationCrypto.name_crypto)
    def get_commod(message: Message):
        if message.text.isdigit():
            result = int(message.text)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['name_crypto'] = spisok_coomod_work[result]
                text = (f'Полученная информация:\n'
                        f'Выбранная криптоволюта:{data['name_crypto']}')
                bot.send_message(message.from_user.id, text)
                api_url = ('https://api.api-ninjas.com/v1/cryptoprice?symbol={}').format(data['name_crypto'])
                response = requests.get(api_url, headers={'X-Api-Key': config.RAPID_API_KEY})
                for i in json.loads(response.text):
                    if i == 'price':
                        result = f'Цена на {data['name_crypto']}:{json.loads(response.text)[i]}'
                        bot.send_message(message.from_user.id, result)
        else:
            bot.send_message(message.from_user.id,f'Нужно указать число, около выбранного наименования. Повторите пожалуйста ввод:')