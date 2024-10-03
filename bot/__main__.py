import random
import os

import telebot

from bot.applications.calculator import bot


# displays a greeting
def greetings(message, btns=None):
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
    bot.send_message(message.chat.id, f"Привет{names}", reply_markup=btns)


@bot.message_handler(commands=["start", "hello"])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton("/about_me")
    btn2 = telebot.types.KeyboardButton("/help")
    markup.row(btn2, btn1)
    markup.add(telebot.types.KeyboardButton("/photo"))
    greetings(message, btns=markup)


# shows all commands
def help(message):
    bot.send_message(
        message.chat.id,
        """<b>команды:</b>              <b>функции:</b>
<u>/start</u>   <u>/hello</u>          начать диалог

<u>/photo</u>                    показать мое фото

<u>/github</u>   <u>/site</u>        показать мой github""",
        parse_mode="html",
    )


@bot.message_handler(commands=["help"])
def show_help(message):
    help(message)


# tell about me
def autobiography(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(
        "программирование", callback_data="програмирование"
    )
    btn2 = telebot.types.InlineKeyboardButton("музыка", callback_data="музыка")
    markup.row(btn1, btn2)
    markup.add(
        telebot.types.InlineKeyboardButton(
            "музыка и программирование", callback_data="музыка и программирование"
        )
    )
    bot.send_message(
        message.chat.id,
        "Меня зовут Егор. Мне 14 лет. В данный момент обучаюсь в 2007 школе. Я люблю музыку и, как уже можно было понять по этому боту, програмировать (номер телефона: 89959039101, дискорд: disaypl)",
        reply_markup=markup,
    )


@bot.message_handler(commands=["about_me"])
def show_autobiography(message):
    autobiography(message)


def tell_about_programming(callback):
    markup = telebot.types.InlineKeyboardMarkup()
    programming = "Сейчас я умею писать только на python. Этого бота написал используя библиотеку pyTelegramBotAPI. Только недавно решил подойти к программированию с полной серьезностью (поэтому вы это и видете). Вот ссылка на мой github"
    markup.add(
        telebot.types.InlineKeyboardButton(
            "мой GitHub", url="https://github.com/KorotEgor"
        )
    )
    bot.send_message(
        callback.message.chat.id,
        f"{programming}<b>↓</b>",
        reply_markup=markup,
        parse_mode="html",
    )


def tell_about_music(callback):
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


@bot.callback_query_handler(func=lambda callback: True)
def callback_about_me(callback):
    if callback.data == "програмирование":
        tell_about_programming(callback)
    elif callback.data == "музыка":
        tell_about_music(callback)
    elif callback.data == "музыка и программирование":
        tell_about_programming(callback)
        tell_about_music(callback)


# responds to photo, video and audio
@bot.message_handler(content_types=["photo", "video", "voice"])
def error_type(message):
    bot.reply_to(message, "Бот не может считывать информацию в таком виде")


# responds to text file
@bot.message_handler(content_types=["document"])
def responds_to_file(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("./user_file.txt", "wb") as new_file:
        new_file.write(downloaded_file)

    if os.path.getsize("./user_file.txt") > 10**6:
        bot.reply_to(message, "Файл слишком большой")
        return

    file = open("./user_file.txt", "r+")

    user_commands = []
    string = file.readline().strip()
    while string:
        user_commands += string.split()
        string = file.readline().strip()

    correct_commands = [
        "/start",
        "/hello",
        "/help",
        "/about_me",
        "/photo",
        "/github",
        "/git",
    ]
    correct_user_commands = []
    for command in user_commands:
        for correct_command in correct_commands:
            usr_comm = command.strip().lower()
            if (
                usr_comm == correct_command.strip()
                and usr_comm not in correct_user_commands
            ):
                correct_user_commands.append(correct_command)

    correct_user_commands = "\n".join(correct_user_commands)
    if correct_user_commands:
        bot.reply_to(
            message,
            f"""Может быть вы хотели ввести эти команды(у):
{correct_user_commands}""",
        )
    else:
        bot.reply_to(message, "Данный файл не содержит команд")
    file.truncate(0)
    file.close()


# show photo
def give_photo(message):
    num = random.randint(1, 6)
    file = open(f"./photos/photo{num}.jpg", "rb")
    bot.send_photo(message.chat.id, file)
    file.close()


@bot.message_handler(commands=["photo"])
def show_my_photo(message):
    give_photo(message)


# opens my github
def open_github(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton(
            "Перейти на мой GitHub", url="https://github.com/KorotEgor"
        )
    )
    bot.send_message(message.chat.id, "Вот мой git", reply_markup=markup)


@bot.message_handler(commands=["github", "git"])
def transfer_to_site(message):
    open_github(message)


# when entering text similar to the corresponding commands, it displays a similar message
@bot.message_handler()
def not_command_text(message):
    if message.text.lower() == "привет":
        greetings(message)
    elif message.text.lower() == "гитхаб":
        open_github(message)
    elif message.text.lower() == "помощь":
        help(message)
    elif message.text.lower() == "фото":
        give_photo(message)
    elif message.text.lower() == "о тебе":
        autobiography(message)


def main():
    bot.polling(non_stop=True)


if __name__ == "__main__":
    main()
