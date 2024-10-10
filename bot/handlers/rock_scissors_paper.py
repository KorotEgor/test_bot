import random
import telebot


def handler(message, bot):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("камень", callback_data="rsp/камень")
    btn2 = telebot.types.InlineKeyboardButton("ножницы", callback_data="rsp/ножницы")
    btn3 = telebot.types.InlineKeyboardButton("бумага", callback_data="rsp/бумага")
    markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Выберите камень, ножницы или бумагу с помощью кнопки", reply_markup=markup)


def change_paper_form(option_for_resp):
    if option_for_resp == "бумага":
        return option_for_resp[:-1] + "у"
    return option_for_resp


def who_wins(user_opt, prog_opt):
    beatings = {
        "rsp/камень": "rsp/ножницы",
        "rsp/ножницы": "rsp/бумага",
        "rsp/бумага": "rsp/камень",
    }
    user_opt_for_resp = user_opt.split("/")[1]
    prog_opt_for_resp = change_paper_form(prog_opt.split("/")[1])
    responce = f'Вы выбрали "{user_opt_for_resp}, а я {prog_opt_for_resp}. '
    if user_opt == prog_opt:
        return responce + "Ничья!"
    elif beatings[user_opt] == prog_opt:
        return responce + "Ты победил!"
    else:
        return responce + "В следующий раз тебе повезет больше!"


def game_callback(callback, bot):
    random_option = random.choice(["rsp/камень", "rsp/ножницы", "rsp/бумага"])
    match callback.data:
        case "rsp/камень":
            response_text = who_wins("rsp/камень", random_option)
        case "rsp/ножницы":
            response_text = who_wins("rsp/ножницы", random_option)
        case "rsp/бумага":
            response_text = who_wins("rsp/бумага", random_option)
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("Да, давай", callback_data="rsprpl/да")
    btn2 = telebot.types.InlineKeyboardButton("Нет, спасибо", callback_data="rsprpl/нет")
    markup.row(btn1, btn2)
    bot.send_message(callback.message.chat.id, f"{response_text} Хотите сыграть еще?", reply_markup=markup)


def reply_game_callback(callback, bot):
    match callback.data:
        case "rsprpl/да":
            handler(callback.message, bot)
        case "rsprpl/нет":
            bot.send_message(callback.message.chat.id, "Хорошо. Спасибо за то, что сыграли")
