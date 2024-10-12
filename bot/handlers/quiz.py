import telebot
from dataclasses import dataclass


@dataclass
class Question:
    question: str
    answers: tuple[str, str, str]
    correct: int


QUESTIONS_AND_ANSWERS = [
    Question(question="Как меня зовут?", answers=("Егор", "Андрей", "Амид"), correct=1),
    Question(question="Сколько мне лет?", answers=("13", "14", "15"), correct=2),
    Question(question="В какой школе я учусь?", answers=("1158", "1488", "2007"), correct=3),
    Question(question="Какую музыку я люблю?", answers=("Металл", "Пост-панк", "Панк"), correct=2),
    Question(
        question="Какими видами спорта я занимался?",
        answers=("Плававнье и футбол", "Хоккей и футбол", "Скалолазанье и футбол"),
        correct=3,
    ),
    Question(question="На каком языке программирования я пишу?", answers=("Python", "C++", "Java"), correct=1),
    Question(question="Какой вид одежды я хочу купить?", answers=("Рубашка", "Пальто", "Джинсовка"), correct=2),
    Question(question="Какой мой любимый цвет?", answers=("Синий", "Красный", "Зеленый"), correct=3),
    Question(question="Какие аниме я посмотрел?", answers=("Наруто", "Адский рай", "Убийца гоблинов"), correct=3),
    Question(
        question="Моя любимая игра? (Есть и другие игры, которые мне тоже очень сильно нравятся)",
        answers=("Sanabi", "The forest", "Stardew Valley"),
        correct=1,
    ),
]


@dataclass
class State:
    question_number: int
    correct_user_answers_count: int


REZULT_END = (
    "Ты меня совсем не знаешь. Хочешь еще раз попробавать?",
    "Ты меня  знаешь. Хочешь еще раз попробавать?" "Ты меня немного знаешь. Хочешь еще раз попробавать?",
    "Ты меня немного знаешь. Хочешь еще раз попробавать?",
    "Мы с тобой только познакомились. Хочешь еще раз попробавать?",
    "Я с тобой почти не общаюсь. Хочешь еще раз попробавать?",
    "Ты меня более мение знаешь. Хочешь еще раз попробавать?",
    "Ты меня знаешь больше 50%. Хочешь еще раз попробавать?",
    "Мы переодически общаемся с тобой. Хочешь еще раз попробавать?",
    "Ты меня знаешь на четверочку. Хочешь еще раз попробавать?",
    "Ты меня знаешь почти идеально. Хочешь еще раз попробавать?",
    "Ты мой лучший друг?",
)


class Quiz:
    def __init__(self):
        self._users = {}

    def show_user_result(self, bot, chat_id, user_id):
        state = self._users[user_id]

        state.question_number = 0
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton("Да", callback_data="qzrpl/да")
        btn2 = telebot.types.InlineKeyboardButton("Нет", callback_data="qzrpl/нет")
        markup.row(btn1, btn2)
        bot.send_message(
            chat_id,
            f"Ты ответил на {state.correct_user_answers_count} вопросов из 10 правильно. {REZULT_END[state.correct_user_answers_count]}",
            reply_markup=markup,
        )
        state.correct_user_answers_count = 0

    def show_question(self, bot, chat_id, question_number):
        answers = QUESTIONS_AND_ANSWERS[question_number].answers
        question = QUESTIONS_AND_ANSWERS[question_number].question
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton(answers[0], callback_data="qz/ответ1")
        btn2 = telebot.types.InlineKeyboardButton(answers[1], callback_data="qz/ответ2")
        btn3 = telebot.types.InlineKeyboardButton(answers[2], callback_data="qz/ответ3")
        btn4 = telebot.types.InlineKeyboardButton("Пропустить", callback_data="qz/пропустить")
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        bot.send_message(chat_id, f"Вопрос {question_number + 1} из 10. {question}", reply_markup=markup)

    def handler(self, message, bot):
        state = self._users.setdefault(message.from_user.id, State(question_number=0, correct_user_answers_count=0))
        self.show_question(bot, message.chat.id, state.question_number)

    def responds_to_option(self, bot, callback, correct_answer, user_answer):
        state = self._users[callback.from_user.id]

        if correct_answer == user_answer:
            bot.send_message(callback.message.chat.id, "Правильно!")
            state.correct_user_answers_count += 1
        else:
            bot.send_message(callback.message.chat.id, "К сожалению это не верно")

    def game_callback(self, callback, bot):
        state = self._users[callback.from_user.id]

        correct = QUESTIONS_AND_ANSWERS[state.question_number].correct
        match callback.data:
            case "qz/ответ1":
                self.responds_to_option(bot, callback, correct, 1)
            case "qz/ответ2":
                self.responds_to_option(bot, callback, correct, 2)
            case "qz/ответ3":
                self.responds_to_option(bot, callback, correct, 3)

        if state.question_number == 9:
            self.show_user_result(
                bot,
                callback.message.chat.id,
                callback.from_user.id,
            )
            return

        state.question_number += 1
        self.show_question(bot, callback.message.chat.id, state.question_number)

    def reply_game_callback(self, callback, bot):
        match callback.data:
            case "qzrpl/да":
                self.handler(callback.message, bot)
            case "qzrpl/нет":
                bot.send_message(callback.message.chat.id, "Хорошо. Спасибо за то, что сыграл")
