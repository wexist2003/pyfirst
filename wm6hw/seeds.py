# pip install Faker
from random import randint, choice
import sqlite3
from faker import Faker
from datetime import datetime
from pprint import pprint
from psycopg2 import Error


disciplines = [
    "Вища математика",
    "Дискретна математика",
    "Лінійна алгебра",
    "Программування",
    "Теорія ймовірності"
    "Історія України",
    "Англійська",
    "Креслення"    
]

groups = [
    "ЕПЗ331",
    "АППВ23",
    "РАПМ3"
]

NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50

fake = Faker()
connect = sqlite3.connect('hw.db')
cur = connect.cursor()

def seed_teachers():
    teachers = [fake.name for _ in range(NUMBER_TEACHERS)]
    sql = "INSERT INTO teachers(fullname) VALUES(?);"
    cur.executemany(sql, zip(teachers,))
    
def seed_disciplines():
    sql = "INSERT INTO disciplines(name, teacher_id) VALUES(?, ?);"
    cur.executemany(sql, zip(disciplines, iter(randint(1, NUMBER_TEACHERS) for _ in range(len(disciplines)))))    

        
if __name__ == '__main__':
    try:
        seed_teachers()
        seed_disciplines()
        connect.commit()
    except sqlite3.Error as error:
        pprint(error)
    finally:
        connect.close()
