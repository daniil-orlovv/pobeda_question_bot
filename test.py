import random as r
import sqlite3 as sql

con = sql.connect("questions.db")
cur = con.cursor()

number = r.randint(20, 35)
cur.execute(f"SELECT question, answer FROM all_questions WHERE number = {number}")
question, answer = cur.fetchone()
print(f"Вопрос: {question}")
print(f"Ответ: {answer}")
