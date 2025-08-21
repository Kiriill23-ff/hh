from loader import bot
from states.commodityprice import InformationCommod
from telebot.types import Message
import requests
from config_data import config
from telebot import types
import json

spisok_coomod_user = (f'1.gold - Фьючерсы на золото\n2.soybean_oil - Фьючерсы на соевое масло\n'
                      f'3.wheat - Фьючерсы на пшеницу\n4.platinum - Платина\n'
                      f'5.micro_silver - Микро-Фьючерсы на Серебро\n6.corn - Фьючерсы на кукурузу\n'
                      f'7.oat - Фьючерсы на Овес\n8.aluminum - Фьючерсы на алюминий\n'
                      f'9.silver - Фьючерсы на серебро\n10.soybean - Фьючерсы на сою\n'
                      f'11.palladium - Палладий\n12.gasoline_rbob - RBOB бензин')
spisok_coomod_work = {1:'gold',2:'soybean_oil',3:'wheat',4:'platinum',
                      5:'micro_silver',6:'corn',7:'oat',8:'aluminum',
                      9:'silver',10:'soybean',11:'palladium',12:'gasoline_rbob'}

@bot.message_handler(commands=["commodityprice"])
def servey(message:Message) -> None:
    bot.set_state(message.from_user.id, InformationCommod.name_commod, message.chat.id)
    bot.send_message(message.from_user.id,text=f'Здравствуйте {message.from_user.username}.Список продуктовых фьючерсов и ценных металлов'
                                               f':\n{spisok_coomod_user} '
                                          f'ввидите цифру стоящую около интересающего вас фьючерса:')

    @bot.message_handler(state=InformationCommod.name_commod)
    def get_commod(message: Message):
        if message.text.isdigit():
            result = int(message.text)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['name_commod'] = spisok_coomod_work[result]
                text = (f'Полученная информация:\n'
                        f'Выбранный фьючерс:{data['name_commod']}')
                bot.send_message(message.from_user.id, text)
                api_url = ('https://api.api-ninjas.com/v1/commodityprice?name={}').format(data['name_commod'])
                response = requests.get(api_url, headers={'X-Api-Key': config.RAPID_API_KEY})
                for i in json.loads(response.text):
                    if i == 'price':
                        result = f'Цена на {data['name_commod']}:{json.loads(response.text)[i]}'
                        bot.send_message(message.from_user.id, result)
        else:
            bot.send_message(message.from_user.id,
                             f'Нужно указать число, около выбранного наименования. Повторите пожалуйста ввод:')