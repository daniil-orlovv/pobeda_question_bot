import os
import random as r
import sqlite3 as sql
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ParseMode
import config

from dotenv import load_dotenv
load_dotenv()


updater = Updater(token=os.getenv('TOKEN'))
con = sql.connect("questions.db", check_same_thread=False)
cur = con.cursor()


def start(update, context):
    """Приветствуем пользователя."""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['Получить вопрос']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, помогу тебе с вопросами!',
        reply_markup=button
        )


def ask_question(update, context):
    """Отправляем вопрос пользователю."""
    number = r.randint(0, 362)
    cur.execute(f"SELECT question, answer FROM all_questions WHERE number = {number}")
    question, answer = cur.fetchone()
    chat = update.effective_chat
    # Создаем встроенную кнопку для получения ответа на вопрос
    button_answer = InlineKeyboardButton(text="Получить ответ", callback_data='button_anwser')
    keyboard = InlineKeyboardMarkup([[button_answer]])
    # Отправляем вопрос пользователю
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

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('ask_question', ask_question))
updater.dispatcher.add_handler(MessageHandler(Filters.text(['Получить вопрос']), ask_question))
updater.dispatcher.add_handler(CallbackQueryHandler(answer_question, pattern="button_anwser"))

updater.start_polling()
updater.idle()
