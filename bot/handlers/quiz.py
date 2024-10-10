import telebot


class Quiz:
    def __init__(self):
        self._question_number = 0
        self._correct_user_answers_count = 0

    def show_user_result(self, message, bot):
        self._question_number = 0
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton("Да", callback_data="qzrpl/да")
        btn2 = telebot.types.InlineKeyboardButton("Нет", callback_data="qzrpl/нет")
        markup.row(btn1, btn2)
        match self._correct_user_answers_count:
            case 0:
                self._correct_user_answers_count = 0
                bot.send_message(
                    message.chat.id,
                    "Ты ответил на 0 вопросов из 10 правильно. Ты меня совсем не знаешь. Хочешь еще раз попробавать?",
                    reply_markup=markup,
                )
            case 1:
                self._correct_user_answers_count = 0
                bot.send_message(
                    message.chat.id,
                    "Ты ответил на 1 вопросов из 10 правильно. Ты меня  знаешь. Хочешь еще раз попробавать?",
                    reply_markup=markup,
                )
            case 2:
                self._correct_user_answers_count = 0
                bot.send_message(
                    message.chat.id,
                    "Ты ответил на 2 вопросов из 10 правильно. Ты меня немного знаешь. Хочешь еще раз попробавать?",
                    reply_markup=markup,
                )
            case 3:
                self._correct_user_answers_count = 0
                bot.send_message(
                    message.chat.id,
                    "Ты ответил на 3 вопросов из 10 правильно. Мы с тобой только познакомились. Хочешь еще раз попробавать?",
                    reply_markup=markup,
                )
            case 4:
                self._correct_user_answers_count = 0
                bot.send_message(
                    message.chat.id,
                    "Ты ответил на 4 вопросов из 10 правильно. Я с тобой почти не общаюсь. Хочешь еще раз попробавать?",
                    reply_markup=markup,
                )
            case 5:
                self._correct_user_answers_count = 0
                bot.send_message(
                    message.chat.id,
                    "Ты ответил на 5 вопросов из 10 правильно. Ты меня более мение знаешь. Хочешь еще раз попробавать?",
                    reply_markup=markup,
                )
            case 6:
                self._correct_user_answers_count = 0
                bot.send_message(
                    message.chat.id,
                    "Ты ответил на 6 вопросов из 10 правильно. Ты меня знаешь больше 50%. Хочешь еще раз попробавать?",
                    reply_markup=markup,
                )
            case 7:
                self._correct_user_answers_count = 0
                bot.send_message(
                    message.chat.id,
                    "Ты ответил на 7 вопросов из 10 правильно. Мы переодически общаемся с тобой. Хочешь еще раз попробавать?",
                    reply_markup=markup,
                )
            case 8:
                self._correct_user_answers_count = 0
                bot.send_message(
                    message.chat.id,
                    "Ты ответил на 8 вопросов из 10 правильно. Ты меня знаешь на четверочку. Хочешь еще раз попробавать?",
                    reply_markup=markup,
                )
            case 9:
                self._correct_user_answers_count = 0
                bot.send_message(
                    message.chat.id,
                    "Ты ответил на 8 вопросов из 10 правильно. Ты меня знаешь почти идеально. Хочешь еще раз попробавать?",
                    reply_markup=markup,
                )
            case 10:
                self._correct_user_answers_count = 0
                bot.send_message(message.chat.id, "Ты ответил на 10 вопросов из 10 правильно. Ты мой лучший друг?")

    def handler(self, message, bot):
        questions_and_answers = [
            {"question": "Как меня зовут?", "answers": ["Егор", "Андрей", "Амид"]},
            {"question": "Сколько мне лет?", "answers": ["13", "14", "15"]},
            {"question": "В какой школе я учусь?", "answers": ["1158", "1488", "2007"]},
            {"question": "Какую музыку я люблю?", "answers": ["Металл", "Пост-панк", "Панк"]},
            {
                "question": "Какими видами спорта я занимался?",
                "answers": ["Плававнье и футбол", "Хоккей и футбол", "Скалолазанье и футбол"],
            },
            {"question": "На каком языке программирования я пишу?", "answers": ["Python", "C++", "Java"]},
            {"question": "Какой вид одежды я хочу купить?", "answers": ["Рубашка", "Пальто", "Джинсовка"]},
            {"question": "Какой мой любимый цвет?", "answers": ["Синий", "Красный", "Зеленый"]},
            {"question": "Какие аниме я посмотрел?", "answers": ["Наруто", "Адский рай", "Убийца гоблинов"]},
            {
                "question": "Моя любимая игра? (Есть и другие игры, которые мне тоже очень сильно нравятся)",
                "answers": ["Sanabi", "The forest", "Stardew Valley"],
            },
        ]

        answers = questions_and_answers[self._question_number]["answers"]
        question = questions_and_answers[self._question_number]["question"]
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton(answers[0], callback_data="qz/ответ1")
        btn2 = telebot.types.InlineKeyboardButton(answers[1], callback_data="qz/ответ2")
        btn3 = telebot.types.InlineKeyboardButton(answers[2], callback_data="qz/ответ3")
        btn4 = telebot.types.InlineKeyboardButton("Пропустить", callback_data="qz/пропустить")
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, f'Вопрос {self._question_number + 1} из 10. {question}', reply_markup=markup)

    def responds_to_option(self, bot, chat_id, correct_answer, user_answer):
        if correct_answer == user_answer:
            bot.send_message(chat_id, "Правильно!")
            self._correct_user_answers_count += 1
        else:
            bot.send_message(chat_id, "К сожалению это не верно")

    def game_callback(self, callback, bot):
        correct_answers = [1, 2, 3, 2, 3, 1, 2, 3, 3, 1]
        match callback.data:
            case "qz/ответ1":
                self.responds_to_option(bot, callback.message.chat.id, correct_answers[self._question_number], 1)
            case "qz/ответ2":
                self.responds_to_option(bot, callback.message.chat.id, correct_answers[self._question_number], 2)
            case "qz/ответ3":
                self.responds_to_option(bot, callback.message.chat.id, correct_answers[self._question_number], 3)
        
        if self._question_number == 9:
            self.show_user_result(
                callback.message,
                bot,
            )
            return
        
        self._question_number += 1
        self.handler(callback.message, bot)

    def reply_game_callback(self, callback, bot):
        match callback.data:
            case "qzrpl/да":
                self.handler(callback.message, bot)
            case "qzrpl/нет":
                bot.send_message(callback.message.chat.id, "Хорошо. Спасибо за то, что сыграл")
