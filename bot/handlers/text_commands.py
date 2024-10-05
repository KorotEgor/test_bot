from bot.handlers import about_me, say_hello, open_github, show_all_commands, give_photo

def handler(message, bot):
    match message.text.lower():
        case "привет":
            say_hello.handler(message, bot)
        case "гитхаб":
            open_github.handler(message, bot)
        case "помощь":
            show_all_commands.handler(message, bot)
        case "фото":
            give_photo.handler(message, bot)
        case "о тебе":
            about_me.autobiography(message)
