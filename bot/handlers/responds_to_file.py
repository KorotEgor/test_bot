import os

def handler(message, bot):
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
            if usr_comm == correct_command.strip() and usr_comm not in correct_user_commands:
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
