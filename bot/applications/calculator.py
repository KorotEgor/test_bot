# expression = ""
# mrk = []


# @bot.message_handler(commands=["calculator"])
# def show_calculator(message, expr=None):
#     markup = telebot.types.InlineKeyboardMarkup()
#     global mrk
#     mrk = markup
#     dig_btn0 = telebot.types.InlineKeyboardButton("0", callback_data="0")
#     dig_btn1 = telebot.types.InlineKeyboardButton("1", callback_data="1")
#     dig_btn2 = telebot.types.InlineKeyboardButton("2", callback_data="2")
#     dig_btn3 = telebot.types.InlineKeyboardButton("3", callback_data="3")
#     dig_btn4 = telebot.types.InlineKeyboardButton("4", callback_data="4")
#     dig_btn5 = telebot.types.InlineKeyboardButton("5", callback_data="5")
#     dig_btn6 = telebot.types.InlineKeyboardButton("6", callback_data="6")
#     dig_btn7 = telebot.types.InlineKeyboardButton("7", callback_data="7")
#     dig_btn8 = telebot.types.InlineKeyboardButton("8", callback_data="8")
#     dig_btn9 = telebot.types.InlineKeyboardButton("9", callback_data="9")
#     del_btn = telebot.types.InlineKeyboardButton("DEL", callback_data="delete")
#     sign_change_btn = telebot.types.InlineKeyboardButton("+/-", callback_data="change sign")
#     conv_to_perc_btn = telebot.types.InlineKeyboardButton("%", callback_data="conversion to percentage")
#     div_btn = telebot.types.InlineKeyboardButton("÷", callback_data="/")
#     mult_btn = telebot.types.InlineKeyboardButton("*", callback_data="*")
#     sub_btn = telebot.types.InlineKeyboardButton("-", callback_data="-")
#     add_btn = telebot.types.InlineKeyboardButton("+", callback_data="+")
#     eql_btn = telebot.types.InlineKeyboardButton("=", callback_data="=")
#     com_btn = telebot.types.InlineKeyboardButton(".", callback_data=".")
#     bracket_btn = telebot.types.InlineKeyboardButton("()", callback_data="()")

#     markup.row(del_btn, sign_change_btn, conv_to_perc_btn, div_btn)
#     markup.row(dig_btn7, dig_btn8, dig_btn9, mult_btn)
#     markup.row(dig_btn4, dig_btn5, dig_btn6, sub_btn)
#     markup.row(dig_btn1, dig_btn2, dig_btn3, add_btn)
#     markup.row(dig_btn0, com_btn, bracket_btn, eql_btn)

#     if expr is None:
#         bot.send_message(message.chat.id, "Введите выражение с помощью кнопок", reply_markup=markup)
#     else:
#         bot.send_message(message.chat.id, expr, reply_markup=markup)


# def change_to_int_or_float(number):
#     if int(number) == number:
#         return str(int(number))
#     else:
#         return str(number)


# def processing_nums(callback):
#     for dig in range(10):
#         if callback.data == str(dig):
#             return str(dig)
#     return ""


# def processing_signs(signs, callback):
#     for sign in signs:
#         if callback.data == sign:
#             return sign

#     return ""


# def processing_all_in_expression(callback, expression):
#     dig_to_add = processing_nums(callback)
#     expression += dig_to_add

#     if callback.data == "()":
#         if not expression or expression[-1] == " ":
#             return ""
#         open_bracket_count = expression.count("(")
#         close_bracket_count = expression.count(")")
#         if open_bracket_count == close_bracket_count:
#             expression += "("
#         else:
#             expression += ")"

#     if not expression:
#         return ""

#     signs = ["+", "-", "*", "/"]
#     sign_to_add = processing_signs(signs, callback)
#     expression += sign_to_add

#     if expression[-1] == " ":
#         return ""

#     first_left_sign = expression.rfind(" ") + 1
#     if callback.data == "change sign":
#         expression = expression[:first_left_sign] + "-" + expression[first_left_sign:]
#     elif callback.data == "conversion to percentage":
#         last_number = float(expression[first_left_sign:])
#         last_number /= 100
#         last_number = change_to_int_or_float(last_number)
#         expression = expression[:first_left_sign] + last_number
#     elif callback.data == ".":
#         expression += "."
#     return expression


# @bot.callback_query_handler(func=lambda callback: True)
# def callback_calculator(callback):
#     global expression
#     expression = processing_all_in_expression(callback, expression)

#     # processing_all_deletes
#     if callback.data == "delete":
#         expression = expression[:-1]

#     if callback.data == "=":
#         solution_of_expression = eval(expression)
#         expression = expression + " = " + str(solution_of_expression)
#         show_calculator(callback.message, expression, after_equal=True)
#         expression = ""
#         return

#     bot.edit_message_text(expression, callback.message.chat.id, callback.message.message_id, reply_markup=mrk)
