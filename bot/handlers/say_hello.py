import telebot

def handler(message, bot):
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton("/about_me")
    btn2 = telebot.types.KeyboardButton("/help")
    markup.row(btn2, btn1)
    markup.add(telebot.types.KeyboardButton("/photo"))
    first_name = message.from_user.last_name
    last_name = message.from_user.first_name
    names = [""]
    if first_name is not None:
        names.append(first_name)
    if last_name is not None:
        names.append(last_name)
    if len(names) > 1:
        names[0] = ","
    names = " ".join(names)
    bot.send_message(message.chat.id, f"Привет{names}", reply_markup=markup)