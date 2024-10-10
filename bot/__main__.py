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
    calculator,
    rock_scissors_paper,
    quiz,
)
import telebot


def main():
    bot = telebot.TeleBot(dotenv_values(".env")["TOKEN"])

    qz = quiz.Quiz()
    bot.register_message_handler(qz.handler, commands=["quiz"], pass_bot=True)
    bot.register_callback_query_handler(qz.game_callback, func=lambda cb: cb.data.startswith("qz/"), pass_bot=True)
    bot.register_callback_query_handler(
        qz.reply_game_callback, func=lambda cb: cb.data.startswith("qzrpl/"), pass_bot=True
    )

    bot.register_message_handler(rock_scissors_paper.handler, commands=["rock_scissors_paper"], pass_bot=True)
    bot.register_callback_query_handler(
        rock_scissors_paper.game_callback, func=lambda cb: cb.data.startswith("rsp/"), pass_bot=True
    )
    bot.register_callback_query_handler(
        rock_scissors_paper.reply_game_callback, func=lambda cb: cb.data.startswith("rsprpl/"), pass_bot=True
    )

    calc = calculator.Calculator()
    bot.register_message_handler(calc.handler, commands=["calculator"], pass_bot=True)
    bot.register_callback_query_handler(calc.callback, func=lambda cb: cb.data.startswith("cal/"), pass_bot=True)

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
