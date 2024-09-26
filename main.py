import random

import telebot
from dotenv import dotenv_values

bot = telebot.TeleBot(dotenv_values(".env")["TOKEN"])

# displays a greeting
def greetings(message, btns=None):
        first_name = message.from_user.last_name
        last_name = message.from_user.first_name
        names = ['']
        if first_name is not None:
                names.append(first_name)
        if first_name is not None:
                names.append(last_name)
        if names:
                names[0] = ','
        names = ' '.join(names)
        bot.send_message(message.chat.id, f'Привет{names}', reply_markup=btns)


@bot.message_handler(commands=['start', 'hello'])
def start(message):
        markup = telebot.types.ReplyKeyboardMarkup()
        btn1 = telebot.types.KeyboardButton('/about_me')
        btn2 = telebot.types.KeyboardButton('/help')
        markup.row(btn2, btn1)
        markup.add(telebot.types.KeyboardButton('/photo'))
        greetings(message, btns=markup)


# shows all commands
def help(message):
        bot.send_message(message.chat.id,
                        '''<b>команды:</b>              <b>функции:</b>
<u>/start</u>   <u>/hello</u>          начать диалог

<u>/photo</u>                    показать мое фото

<u>/github</u>   <u>/site</u>        показать мой github
<u>/website</u>   <u>/git</u>''',
parse_mode='html'
)


@bot.message_handler(commands=['help'])
def show_help(message):
        help(message)


# tell about me
def autobiography(message):
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton('программирование', callback_data='програмирование')
        btn2 = telebot.types.InlineKeyboardButton('музыка', callback_data='музыка')
        markup.row(btn1, btn2)
        markup.add(telebot.types.InlineKeyboardButton('музыка и программирование', callback_data='музыка и программирование'))
        bot.send_message(message.chat.id, 'Меня зовут Егор. Мне 14 лет. В данный момент обучаюсь в 2007 школе. Я люблю музыку и, как уже можно было понять по этому боту, програмировать (номер телефона: 89959039101, дискорд: disaypl)', reply_markup=markup)


@bot.message_handler(commands=['about_me'])
def show_autobiography(message):
        autobiography(message)


def tell_about_programming(callback):
        markup = telebot.types.InlineKeyboardMarkup()
        programming = 'Сейчас я умею писать только на python. Этого бота написал используя библиотеку pyTelegramBotAPI. Только недавно решил подойти к программированию с полной серьезностью (поэтому вы это и видете). Вот ссылка на мой github'
        markup.add(telebot.types.InlineKeyboardButton('мой GitHub', url='https://github.com/KorotEgor'))
        bot.send_message(callback.message.chat.id, f'{programming}<b>↓</b>', reply_markup=markup, parse_mode='html')


def tell_about_music(callback):
        markup = telebot.types.InlineKeyboardMarkup()
        music = 'В основном слущаю пост-панк и панк-рок. У меня нет единственного либимого исполнителя или единственной любимой песни. Исполнители, которых я могу посоветовать: Сова, Черный Лукич, Янка Дигелева, Перемотка, Свидетельство о смерти и много кого еще. Если интересно вот ссылка на мой плейлист на яндекс музыке'
        markup.add(telebot.types.InlineKeyboardButton('плейлист на яндекс музыке', url='https://music.yandex.ru/users/KorEgor10/playlists/1005'))
        bot.send_message(callback.message.chat.id, f'{music}<b>↓</b>', reply_markup=markup, parse_mode='html')  


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
        if callback.data == 'програмирование':
                tell_about_programming(callback)
        elif callback.data == 'музыка':
                tell_about_music(callback)
        elif callback.data == 'музыка и программирование':
                tell_about_programming(callback)
                tell_about_music(callback)


# responds to photo
@bot.message_handler(content_types=['photo'])
def responds_to_photo(message):
        bot.reply_to(message, '<b>Зачем ты мне это отправил?</b>', parse_mode='html')


# show photo
def give_photo(message):
        num = random.randint(1, 6)
        file = open(f'./photos/photo{num}.jpg', 'rb')
        bot.send_photo(message.chat.id, file)
        file.close()


@bot.message_handler(commands=['photo'])
def show_my_photo(message):
        give_photo(message)


# opens my github
def open_github(message):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Перейти на мой GitHub', url='https://github.com/KorotEgor'))
        bot.send_message(message.chat.id, 'Вот мой git', reply_markup=markup)


@bot.message_handler(commands=['github', 'site', 'website', 'git'])
def transfer_to_site(message):
        open_github(message)


# when entering text similar to the corresponding commands, it displays a similar message
@bot.message_handler()
def not_command_text(message):
        if message.text.lower() == 'привет':
                greetings(message)
        elif message.text.lower() == 'гитхаб':
                open_github(message)
        elif message.text.lower() == 'помощь':
                help(message)
        elif message.text.lower() == 'фото':
                give_photo(message)
        elif message.text.lower() == 'о тебе':
                autobiography(message)

bot.polling(non_stop=True)