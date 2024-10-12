import telebot
from dataclasses import dataclass

# dependencies = {
#     'digs': ['signs', '.', '%', '+/-', 'DEL'],
#     'signs': ['digs', 'DEL'],
#     '.': ['digs', 'DEL'],
#     '%': ['digs', 'signs','DEL']

# }


@dataclass
class State:
    expression: str
    mrk: telebot.types.InlineKeyboardMarkup


class Calculator:
    def __init__(self):
        self._users = {}

    def handler(self, message, bot):
        mrk = telebot.util.quick_markup(
            {
                "DEL": {"callback_data": "cal/delete"},
                "+/-": {"callback_data": "cal/change sign"},
                "%": {"callback_data": "cal/conversion to percentage"},
                "÷": {"callback_data": "cal//"},
                "7": {"callback_data": "cal/7"},
                "8": {"callback_data": "cal/8"},
                "9": {"callback_data": "cal/9"},
                "*": {"callback_data": "cal/*"},
                "4": {"callback_data": "cal/4"},
                "5": {"callback_data": "cal/5"},
                "6": {"callback_data": "cal/6"},
                "-": {"callback_data": "cal/-"},
                "1": {"callback_data": "cal/1"},
                "2": {"callback_data": "cal/2"},
                "3": {"callback_data": "cal/3"},
                "+": {"callback_data": "cal/+"},
                "0": {"callback_data": "cal/0"},
                ".": {"callback_data": "cal/."},
                "=": {"callback_data": "cal/="},
            },
            row_width=4,
        )

        state = self._users.setdefault(message.from_user.id, State(expression="", mrk=mrk))

        if not state.expression:
            bot.send_message(message.chat.id, "Введите выражение с помощью кнопок", reply_markup=state.mrk)
        else:
            bot.send_message(message.chat.id, state.expression, reply_markup=state.mrk)

    def processing_all_in_expression(self, cmd, expression):
        dig_to_add = processing_nums(cmd)
        expression += dig_to_add

        if not expression:
            return ""

        signs = ["+", "-", "*", "/"]
        sign_to_add = processing_signs(signs, cmd)
        expression += sign_to_add

        if expression[-1] == " ":
            return ""

        first_left_sign = expression.rfind(" ") + 1
        if cmd == "change sign":
            expression = expression[:first_left_sign] + "-" + expression[first_left_sign:]
        elif cmd == "conversion to percentage":
            last_number = float(expression[first_left_sign:])
            last_number /= 100
            last_number = change_to_int_or_float(last_number)
            expression = expression[:first_left_sign] + last_number
        elif cmd == ".":
            expression += "."

        return expression

    def callback(self, callback, bot):
        state = self._users[callback.from_user.id]

        cmd = callback.data.removeprefix("cal/")
        state.expression = self.processing_all_in_expression(cmd, state.expression)

        # processing_all_deletes
        if cmd == "delete":
            state.expression = state.expression[:-1]

        if cmd == "=":
            solution_of_expression = eval(state.expression)
            state.expression = state.expression + " = " + str(solution_of_expression)
            bot.edit_message_text(
                state.expression, callback.message.chat.id, callback.message.message_id, reply_markup=state.mrk
            )
            state.expression = ""
            return

        bot.edit_message_text(
            state.expression, callback.message.chat.id, callback.message.message_id, reply_markup=state.mrk
        )


def change_to_int_or_float(number):
    if int(number) == number:
        return str(int(number))
    else:
        return str(number)


def processing_nums(cmd):
    for dig in range(10):
        if cmd == str(dig):
            return str(dig)
    return ""


def processing_signs(signs, cmd):
    for sign in signs:
        if cmd == sign:
            return sign

    return ""
