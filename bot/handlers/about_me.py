import telebot

def handler(message, bot):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("программирование", callback_data="програмирование")
    btn2 = telebot.types.InlineKeyboardButton("музыка", callback_data="музыка")
    markup.row(btn1, btn2)
    markup.add(
        telebot.types.InlineKeyboardButton("музыка и программирование", callback_data="музыка и программирование")
    )
    bot.send_message(
        message.chat.id,
        "Меня зовут Егор. Мне 14 лет. В данный момент обучаюсь в 2007 школе. Я люблю музыку и, как уже можно было понять по этому боту, програмировать (номер телефона: 89959039101, дискорд: disaypl)",
        reply_markup=markup,
    )


def tell_about_programming(callback, bot):
    markup = telebot.types.InlineKeyboardMarkup()
    programming = "Сейчас я умею писать только на python. Этого бота написал используя библиотеку pyTelegramBotAPI. Только недавно решил подойти к программированию с полной серьезностью (поэтому вы это и видете). Вот ссылка на мой github"
    markup.add(telebot.types.InlineKeyboardButton("мой GitHub", url="https://github.com/KorotEgor"))
    bot.send_message(
        callback.message.chat.id,
        f"{programming}<b>↓</b>",
        reply_markup=markup,
        parse_mode="html",
    )


def tell_about_music(callback, bot):
    markup = telebot.types.InlineKeyboardMarkup()
    music = "В основном слущаю пост-панк и панк-рок. У меня нет единственного либимого исполнителя или единственной любимой песни. Исполнители, которых я могу посоветовать: Сова, Черный Лукич, Янка Дигелева, Перемотка, Свидетельство о смерти и много кого еще. Если интересно вот ссылка на мой плейлист на яндекс музыке"
    markup.add(
        telebot.types.InlineKeyboardButton(
            "плейлист на яндекс музыке",
            url="https://music.yandex.ru/users/KorEgor10/playlists/1005",
        )
    )
    bot.send_message(
        callback.message.chat.id,
        f"{music}<b>↓</b>",
        reply_markup=markup,
        parse_mode="html",
    )


def callback(callback, bot):
    if callback.data == "програмирование":
        tell_about_programming(callback, bot)
    elif callback.data == "музыка":
        tell_about_music(callback, bot)
    elif callback.data == "музыка и программирование":
        tell_about_programming(callback, bot)
        tell_about_music(callback, bot)
