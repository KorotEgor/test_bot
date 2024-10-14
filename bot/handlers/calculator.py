from dataclasses import dataclass
import telebot


PERMITTED_OPERATIONS = {
    "digs": ["digs", "signs", ".", "change sign"],
    "signs": ["digs"],
    ".": ["digs", "change sign"],
    "change sign": ["change sign", "digs", ".", "signs"],
}


@dataclass
class State:
    expression: list
    all_operations: list
    markup: telebot.types.InlineKeyboardMarkup


class Calculator:
    def __init__(self):
        self._users = {}

    def handler(self, message, bot):
        markup = telebot.util.quick_markup(
            {
                "÷": {"callback_data": "cal//"},
                "-": {"callback_data": "cal/-"},
                "+": {"callback_data": "cal/+"},
                "*": {"callback_data": "cal/*"},
                "7": {"callback_data": "cal/7"},
                "8": {"callback_data": "cal/8"},
                "9": {"callback_data": "cal/9"},
                "+/-": {"callback_data": "cal/change sign"},
                "4": {"callback_data": "cal/4"},
                "5": {"callback_data": "cal/5"},
                "6": {"callback_data": "cal/6"},
                "=": {"callback_data": "cal/="},
                "1": {"callback_data": "cal/1"},
                "2": {"callback_data": "cal/2"},
                "3": {"callback_data": "cal/3"},
                ".": {"callback_data": "cal/."},
                "0": {"callback_data": "cal/0"},
            },
            row_width=4,
        )

        state = self._users.setdefault(message.from_user.id, State(expression=[], all_operations=[], markup=markup))
        if state.expression:
            bot.send_message(message.chat.id, state.expression, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Введите выражение с помощью кнопок", reply_markup=state.markup)

    def callback(self, callback, bot):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id
        user_id = callback.from_user.id
        state = self._users[user_id]

        data = callback.data.removeprefix("cal/")
        data_to_compare = change_to_compare(data)
        exp = state.expression

        some_changes = False
        if exp:
            last_operation = state.all_operations[-1]
            is_permitted_operation = data_to_compare in PERMITTED_OPERATIONS[last_operation]
        else:
            last_operation = None
            is_permitted_operation = False

        match data:
            case "change sign":
                if is_permitted_operation:
                    state.all_operations.append(data_to_compare)
                    self.change_sign(user_id)
                    some_changes = True
            case "=":
                self.processing_equals(user_id, bot, chat_id, message_id, last_operation)
                return
            case _:
                if is_permitted_operation or (not exp and data_to_compare == "digs"):
                    state.all_operations.append(data_to_compare)
                    some_changes = self.add_to_expression(user_id, data)
                    if not some_changes:
                        state.all_operations = state.all_operations[:-1]
        if some_changes:
            bot.edit_message_text(' '.join(exp), chat_id, message_id, reply_markup=state.markup)

    def change_sign(self, user_id):
        state = self._users[user_id]
        last_added = state.expression[-1]
        if last_added[0] == "-":
            state.expression[-1] = last_added[1:]
        else:
            state.expression[-1] = "-" + last_added

    def processing_equals(self, user_id, bot, chat_id, message_id, last_operation):
        state = self._users[user_id]
        exp = state.expression
        if (last_operation == "digs" or last_operation == "change sign") and "signs" in state.all_operations:
            str_exp = " ".join(exp)
            solution_of_expression = eval(str_exp)
            state.expression = str_exp + " = " + str(solution_of_expression)
            bot.edit_message_text(state.expression, chat_id, message_id, reply_markup=state.markup)
            state.expression = []
            state.all_operations = []

    def add_to_expression(self, user_id, data):
        state = self._users[user_id]
        is_zero = data == '0'
        if not state.expression:
            if is_zero:
                return False
            state.expression.append(data)
            return True
        operations = state.all_operations
        if is_num_or_pnt(operations[-2]) and is_num_or_pnt(operations[-1]):
            state.expression[-1] += data
        else:
            if is_zero:
                return False
            state.expression.append(data)
        return True


def is_num_or_pnt(operation):
    if operation == 'digs' or operation == '.':
        return True
    return False


def change_to_compare(data):
    if "0" <= data <= "9":
        return "digs"
    elif data in ["+", "-", "/", "*"]:
        return "signs"
    else:
        return data
