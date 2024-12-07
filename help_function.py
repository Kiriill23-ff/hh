from datetime import datetime
import re


format_phone = r'^7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$'
format_mail = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.ru$'
format_date_1 = "%d.%m.%Y"
format_date_2 = "%Y-%m-%d"

def validate_date(date):

    """Validate date"""
    try:
        if bool(datetime.strptime(date, format_date_1)):
            return 'FIELD_TYPE'
        elif bool(datetime.strptime(date, format_date_2)):
            return 'FIELD_TYPE'
    except ValueError:
       return 'NO VALIDATE'

def validate_phone(number_phone):
    """Validate phone"""

    if bool(re.match(format_phone,number_phone)):
        return 'FIELD_TYPE'
    else:
        return 'NO VALIDATE'

def validate_email(email):
    """Validate phone"""

    if bool(re.match(format_mail,email)):
        return 'FIELD_TYPE'
    else:
        return 'NO VALIDATE'

def validation_form(dict_on_validation):

    """Function start validate"""

    dictionary_length = len(dict_on_validation)
    list_dict_on_value_validate = list(dict_on_validation.values())
    list_dict_on_keys_validate = list(dict_on_validation.keys())
    result_dict = {}
    if dictionary_length == 1:
        date = list_dict_on_value_validate[0]
        result_validate_date = validate_date(date)
        result_dict[list_dict_on_keys_validate[0]] = result_validate_date

    elif dictionary_length == 2:
        date = list_dict_on_value_validate[0]
        phone = list_dict_on_value_validate[1]
        result_validate_date = validate_date(date)
        result_dict[list_dict_on_keys_validate[0]] = result_validate_date
        result_validate_phone = validate_phone(phone)
        result_dict[list_dict_on_keys_validate[1]] = result_validate_phone
    else:
        date = list_dict_on_value_validate[0]
        phone = list_dict_on_value_validate[1]
        email = list_dict_on_value_validate[2]
        result_validate_date = validate_date(date)
        result_dict[list_dict_on_keys_validate[0]] = result_validate_date
        result_validate_phone = validate_phone(phone)
        result_dict[list_dict_on_keys_validate[1]] = result_validate_phone
        result_validate_email = validate_email(email)
        result_dict[list_dict_on_keys_validate[2]] = result_validate_email

    return result_dict