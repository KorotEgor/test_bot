from dotenv import dotenv_values
from bot.handlers import (
    text_commands,
    open_github,
    give_photo,
    responds_to_file,
    responds_to_error_file_types,
    show_all_commands,
    say_hello,
    about_me,
)
import telebot


def main():
    bot = telebot.TeleBot(dotenv_values(".env")["TOKEN"])

    bot.register_message_handler(about_me.handler, commands=["about_me"], pass_bot=True)
    bot.register_callback_query_handler(about_me.callback, func=lambda cb: cb.data.startswith("me/"), pass_bot=True)

    bot.register_message_handler(say_hello.handler, commands=["start", "hello"], pass_bot=True)
    bot.register_message_handler(show_all_commands.handler, commands=["help"], pass_bot=True)
    bot.register_message_handler(
        responds_to_error_file_types.handler,
        content_types=["photo", "video", "voice"],
        pass_bot=True,
    )
    bot.register_message_handler(responds_to_file.handler, content_types=["document"], pass_bot=True)
    bot.register_message_handler(give_photo.handler, commands=["photo"], pass_bot=True)
    bot.register_message_handler(open_github.handler, commands=["github", "git"], pass_bot=True)
    bot.register_message_handler(text_commands.handler, pass_bot=True)

    bot.polling(non_stop=True)


if __name__ == "__main__":
    main()
