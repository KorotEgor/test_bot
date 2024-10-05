import random


def handler(message, bot):
    num = random.randint(1, 6)
    with open(f"./static/photos/photo{num}.jpg", "rb") as file:
        bot.send_photo(message.chat.id, file)
