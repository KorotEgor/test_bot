def handler(message, bot):
    bot.send_message(
        message.chat.id,
        '''<b>команды:</b>              <b>функции:</b>
<u>/start</u>   <u>/hello</u>                    начать диалог

<u>/photo</u>                                показать мое фото

<u>/github</u>   <u>/site</u>                    показать мой github

<u>/about_me</u>                        рассказать обо мне

<u>/calculator</u>                         показать калькулятор

<u>/rock_scissors_paper</u>     игра "камень, ножницы, бумага"''',
        parse_mode="html",
    )
