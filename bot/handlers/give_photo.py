import random

def handler(message, bot):
    num = random.randint(1, 6)
    file = open(f"./static/photos/photo{num}.jpg", "rb")
    bot.send_photo(message.chat.id, file)
    file.close()