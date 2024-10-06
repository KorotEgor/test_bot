def handler(message, bot):
    file_info = bot.get_file(message.document.file_id)
    if file_info.file_size > 10**3:
        bot.reply_to(message, "Файл слишком большой")
        return

    data = bot.download_file(file_info.file_path)

    correct_commands = {
        "start",
        "hello",
        "help",
        "about_me",
        "photo",
        "github",
        "git",
    }

    correct_user_commands = set()
    lines = [string.strip() for string in data.decode().split("\n")]
    for line in lines:
        for cmd in line.split():
            cmd = cmd.strip().removeprefix("/").lower()
            if cmd in correct_commands:
                correct_user_commands.add("/" + cmd)

    correct_user_commands = "\n".join(correct_user_commands)
    if correct_user_commands:
        bot.reply_to(
            message,
            f"""Может быть вы хотели ввести эти команды(у):
{correct_user_commands}""",
        )
    else:
        bot.reply_to(message, "Данный файл не содержит команд")
