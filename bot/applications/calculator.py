from bot.__main__ import bot

import telebot

expression = {
    'numbers': [],
    'signs': {},
    'number_bracket': {'(': [], ')': []},
    'string_expression': [],
}


@bot.message_handler(commands=['calculator'])
def show_calculator(message):
    markup = telebot.types.InlineKeyboardMarkup()
    dig_btn0 = telebot.types.InlineKeyboardButton("0", callback_data="0")
    dig_btn1 = telebot.types.InlineKeyboardButton("1", callback_data="1")
    dig_btn2 = telebot.types.InlineKeyboardButton("2", callback_data="2")
    dig_btn3 = telebot.types.InlineKeyboardButton("3", callback_data="3")
    dig_btn4 = telebot.types.InlineKeyboardButton("4", callback_data="4")
    dig_btn5 = telebot.types.InlineKeyboardButton("5", callback_data="5")
    dig_btn6 = telebot.types.InlineKeyboardButton("6", callback_data="6")
    dig_btn7 = telebot.types.InlineKeyboardButton("7", callback_data="7")
    dig_btn8 = telebot.types.InlineKeyboardButton("8", callback_data="8")
    dig_btn9 = telebot.types.InlineKeyboardButton("9", callback_data="9")
    del_btn = telebot.types.InlineKeyboardButton("DEL", callback_data="delete")
    sign_change_btn = telebot.types.InlineKeyboardButton("+/-", callback_data="change sign")
    conv_to_perc_btn = telebot.types.InlineKeyboardButton("%", callback_data="conversion to percentage")
    div_btn = telebot.types.InlineKeyboardButton("÷", callback_data="/")
    mult_btn = telebot.types.InlineKeyboardButton("·", callback_data="*")
    sub_btn = telebot.types.InlineKeyboardButton("-", callback_data="-")
    add_btn = telebot.types.InlineKeyboardButton("+", callback_data="+")
    eql_btn = telebot.types.InlineKeyboardButton("=", callback_data="=")
    com_btn = telebot.types.InlineKeyboardButton(".", callback_data=".")
    bracket_btn = telebot.types.InlineKeyboardButton("()", callback_data="()")

    markup.row(del_btn, sign_change_btn, conv_to_perc_btn, div_btn)
    markup.row(dig_btn7, dig_btn8, dig_btn9, mult_btn)
    markup.row(dig_btn4, dig_btn5, dig_btn6, sub_btn)
    markup.row(dig_btn1, dig_btn2, dig_btn3, add_btn)
    markup.row(dig_btn0, com_btn, bracket_btn, eql_btn)

    bot.send_message(message.chat.id, 'Введите выражение с помощью кнопок', reply_markup=markup)


def change_last_char(char):
    expression['last_char'].append(char)


def delete_last_char():
    if not expression['last_char']:
        return
    expression['last_char'].pop(-1)


def add_int_or_float_number(num):
    numbers = expression['numbers']
    if int(num) == num:
        numbers.append(int(num))
    else:
        numbers.append(num)


def processing_nums(callback):
    for dig in range(0, 10):
        numbers_count = len(expression["numbers"])
        signs_count = len(expression["signs"])
        if callback.data == dig and numbers_count == signs_count:
            expression['numbers'].append(dig)
            change_last_char(dig)
            return
        elif callback.data == dig and numbers_count > signs_count:
            expression['numbers'][numbers_count - 1] += dig
            change_last_char(dig)
            return


def processing_signs(signs, callback):
    for sign in signs:
        numbers_count = len(expression["numbers"])
        signs_count = len(expression["signs"])
        if callback.data == sign and numbers_count == signs_count:
            return
        elif callback.data == sign and numbers_count > signs_count:
            expression['signs'].append(sign)
            change_last_char(sign)
            return


def processing_all_in_expression(callback, numbers, number_bracket, signs):
    processing_nums(
        callback
    )

    if callback.data == '()':
        if not len(numbers):
            number_bracket['('].append(len(numbers))
            change_last_char('()')
        elif len(number_bracket['(']) == len(number_bracket[')']):
            number_bracket['('].append(len(numbers) - 1)
            change_last_char('()')
        elif len(number_bracket['(']) > len(number_bracket[')']) and numbers[-1] == signs[-1]:
            return
        elif len(number_bracket['(']) > len(number_bracket[')']) and numbers[-1] > signs[-1]:
            number_bracket[')'].append(len(numbers) - 1)
            change_last_char('()')

    
    if not numbers:
        return
    
    check_signs = [
        '+',
        '-',
        '*',
        '/'
    ]
    processing_signs(
        check_signs,
        callback
    )

    last_number = numbers[-1]
    if callback.data == 'change sign':
        numbers[-1] = '-' + last_number
        change_last_char('+/-')
    elif callback.data == 'conversion to percentage' and not numbers:
        last_number = float(last_number) // 100
        add_int_or_float_number(last_number)
        change_last_char('%')
    elif callback.data == '.':
        numbers[-1] = last_number + '.'
        change_last_char('.')


def processing_all_deletes(callback, numbers, number_bracket, signs):
    last_character = expression['last_char'][-1]
    if callback.data == 'delete':
        if '0' <= last_character <= '9' or last_character == '.':
            numbers[-1] = numbers[-1][:-1]
        elif last_character == '+/-':
            numbers[-1] = numbers[-1][1:]
        elif last_character == '%':
            last_number *= 100
            add_int_or_float_number(last_number)
        elif last_character in signs :
            exp_signs = expression['signs']
            exp_signs.pop(len(exp_signs))
        elif last_character == '()':
            number_bracket.pop(len(number_bracket))
        delete_last_char()


def calculate_expression():
    brackets = expression['number_bracket']
    if brackets:
        for i in range(brackets['('][-1], brackets[')'][-1] + 1):

        return calculate_expression()


def show_expression(callback):
    str_exp = ''
    for i in range(len(expression['signs'])):
        str_exp += expression.get(i)

    bot.edit_message_text(
        callback.message.chat.id,
        callback.message.message_id
    )


@bot.callback_query_handler(func=lambda callback: True)
def callback_calculator(callback):
    numbers = expression["numbers"]
    number_bracket = expression['number_bracket']
    signs = expression['signs']

    processing_all_in_expression(callback, numbers, number_bracket, signs)

    processing_all_deletes(callback, numbers, number_bracket, signs)
    
    if callback.data == '=':
        if len(number_bracket) % 2 == 1:
            number_bracket.pop(len(number_bracket))
        nums = []
