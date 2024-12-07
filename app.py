from tinydb import TinyDB, Query
from flask import Flask, request

database = TinyDB('useer.db')


def search_in_bd(search_form):
    result_search_in_bd = database.search(Query().fragment(search_form))
    return result_search_in_bd


def create_bd():
    """Function create form in db"""

    database.default_table_name = 'Forms-versions'
    database.insert_multiple(
        [{'name': 'New form', "email_var_1_1": 'email', "phone_var_1_2": "phone", "text_var_1_3": "text"},
         {'name': 'For second', "phone_var_2_2": "phone"}, {'name': 'third form', "email_var_3_1": 'email'},
         {'name': 'fourth form', "text_var_4_3": "text"},
         {'name': 'fifth form', "email_var_5_1": 'email', "phone_var_1_2": "phone"}])


def create_app():
    create_bd()
    """Create Flask"""
    app = Flask(__name__)

    @app.route("/get_form", methods=['POST'])
    def func_get_form():
        info_url = request.values
        result_search = search_in_bd(info_url)
        if result_search:
            display = result_search[0].get('name')
            return f'Найдено совпадение! Название совпавшей формы {display}'
        else:
            from help_function import validation_form
            result_dict = validation_form(info_url)
            return result_dict

    return app
