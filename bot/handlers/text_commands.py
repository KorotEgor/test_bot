from bot.handlers import old

def handler(message):
    if message.text.lower() == "привет":
        old.greetings(message)
    elif message.text.lower() == "гитхаб":
        old.open_github(message)
    elif message.text.lower() == "помощь":
        old.help(message)
    elif message.text.lower() == "фото":
        old.give_photo(message)
    elif message.text.lower() == "о тебе":
        old.autobiography(message)
