from telebot.handler_backends import State,StatesGroup


class InformationMortage(StatesGroup):
    cost = State()
    procent = State()
    years = State()


