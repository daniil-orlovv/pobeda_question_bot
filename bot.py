import os
import random as r
import sqlite3 as sql
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                          MessageHandler, Filters)
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton,
                      ReplyKeyboardMarkup, ParseMode)

from dotenv import load_dotenv
load_dotenv()


updater = Updater(token=os.getenv('TOKEN'))
con = sql.connect("questions.db", check_same_thread=False)
cur = con.cursor()


def start(update, context):
    """Приветствуем пользователя."""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [['Получить любой вопрос', 'Вопросы по разделам']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, помогу тебе с вопросами!',
        reply_markup=button
        )


def back(update, context):
    """Вернуться назад."""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [['Получить любой вопрос', 'Вопросы по разделам']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Выбери вариант:',
        reply_markup=button
        )


def ask_all_question(update, context):
    """Отправляем вопрос пользователю."""
    number = r.randint(0, 362)
    cur.execute(
        f"SELECT question, answer FROM all_questions WHERE number = {number}")
    question, answer = cur.fetchone()
    chat = update.effective_chat
    button_answer = InlineKeyboardButton(
        text="Получить ответ",
        callback_data='button_anwser'
    )
    keyboard = InlineKeyboardMarkup([[button_answer]])
    context.bot.send_message(
        chat_id=chat.id,
        text=question,
        reply_markup=keyboard
    )
    context.chat_data['answer_key'] = answer
    context.chat_data['question_key'] = question


def other_questions(update, context):
    """Отправляем кнопки пользователю."""
    chat = update.effective_chat
    buttons = ReplyKeyboardMarkup(
        [['Стандартные операционные процедуры',
          'Аварийно – спасательные процедуры'],
         ['Аварийно – спасательное оборудование',
         'Конструкция ВС'],
         ['Оказание первой помощи'],
         ['Назад']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Выбери категорию вопросов:',
        reply_markup=buttons
        )


def questions_one(update, context):
    """Отправляем вопрос пользователю из раздела стандартных операционных
        процедур.
        """
    number = r.randint(0, 106)
    cur.execute(
        f"SELECT question, answer FROM all_questions WHERE number = {number}")
    question, answer = cur.fetchone()
    chat = update.effective_chat
    button_answer = InlineKeyboardButton(
        text="Получить ответ",
        callback_data='button_anwser'
        )
    keyboard = InlineKeyboardMarkup([[button_answer]])
    context.bot.send_message(
        chat_id=chat.id,
        text=question,
        reply_markup=keyboard
    )
    context.chat_data['answer_key'] = answer
    context.chat_data['question_key'] = question


def questions_two(update, context):
    """Отправляем вопрос пользователю из раздела аварийно – спасательных
        процедур.
        """
    number = r.randint(107, 200)
    cur.execute(
        f"SELECT question, answer FROM all_questions WHERE number = {number}")
    question, answer = cur.fetchone()
    chat = update.effective_chat
    button_answer = InlineKeyboardButton(
        text="Получить ответ",
        callback_data='button_anwser'
    )
    keyboard = InlineKeyboardMarkup([[button_answer]])
    context.bot.send_message(
        chat_id=chat.id,
        text=question,
        reply_markup=keyboard
    )
    context.chat_data['answer_key'] = answer
    context.chat_data['question_key'] = question


def questions_three(update, context):
    """Отправляем вопрос пользователю из раздела аварийно – спасательного
        оборудования.
        """
    number = r.randint(200, 229)
    cur.execute(
        f"SELECT question, answer FROM all_questions WHERE number = {number}")
    question, answer = cur.fetchone()
    chat = update.effective_chat
    button_answer = InlineKeyboardButton(
        text="Получить ответ",
        callback_data='button_anwser'
    )
    keyboard = InlineKeyboardMarkup([[button_answer]])
    context.bot.send_message(
        chat_id=chat.id,
        text=question,
        reply_markup=keyboard
    )
    context.chat_data['answer_key'] = answer
    context.chat_data['question_key'] = question


def questions_four(update, context):
    """Отправляем вопрос пользователю из раздела конструкция ВС."""
    number = r.randint(230, 332)
    cur.execute(
        f"SELECT question, answer FROM all_questions WHERE number = {number}")
    question, answer = cur.fetchone()
    chat = update.effective_chat
    button_answer = InlineKeyboardButton(
        text="Получить ответ",
        callback_data='button_anwser'
    )
    keyboard = InlineKeyboardMarkup([[button_answer]])
    context.bot.send_message(
        chat_id=chat.id,
        text=question,
        reply_markup=keyboard
    )
    context.chat_data['answer_key'] = answer
    context.chat_data['question_key'] = question


def questions_five(update, context):
    """Отправляем вопрос пользователю из раздела оказание первой помощи."""
    number = r.randint(333, 362)
    cur.execute(
        f"SELECT question, answer FROM all_questions WHERE number = {number}")
    question, answer = cur.fetchone()
    chat = update.effective_chat
    button_answer = InlineKeyboardButton(
        text="Получить ответ",
        callback_data='button_anwser'
    )
    keyboard = InlineKeyboardMarkup([[button_answer]])
    context.bot.send_message(
        chat_id=chat.id,
        text=question,
        reply_markup=keyboard
    )
    context.chat_data['answer_key'] = answer
    context.chat_data['question_key'] = question


def answer_question(update, context):
    """Отправляем ответ пользователю на вопрос."""
    answer = context.chat_data.get('answer_key')
    question = context.chat_data.get('question_key')
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f'{question}\n\n<b>{answer}</b>',
        parse_mode=ParseMode.HTML
        )


updater.dispatcher.add_handler(CommandHandler(
    'start',
    start
    )
)
updater.dispatcher.add_handler(CommandHandler(
    'ask_question',
    ask_all_question
    )
)
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    ['Получить любой вопрос']),
    ask_all_question)
)
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    ['Назад']),
    back)
)
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    ['Вопросы по разделам']),
    other_questions)
)
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    ['Стандартные операционные процедуры']),
    questions_one)
)
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    ['Аварийно – спасательные процедуры']),
    questions_two)
)
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    ['Аварийно – спасательное оборудование']),
    questions_three)
)
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    ['Конструкция ВС']),
    questions_four)
)
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    ['Оказание первой помощи']),
    questions_five)
)
updater.dispatcher.add_handler(CallbackQueryHandler(
    answer_question,
    pattern="button_anwser")
)

updater.start_polling()
updater.idle()
