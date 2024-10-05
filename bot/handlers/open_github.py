import telebot

def handler(message, bot):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Перейти на мой GitHub", url="https://github.com/KorotEgor"))
    bot.send_message(message.chat.id, "Вот мой git", reply_markup=markup)