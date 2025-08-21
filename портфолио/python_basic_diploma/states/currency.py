from telebot.handler_backends import State,StatesGroup

class InformationCurrency(StatesGroup):
    current_currency = State()
    get_currency = State()
    summ_currency = State()
