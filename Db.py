

import sqlite3

from telebot.util import user_link

conn = sqlite3.connect('user.db', check_same_thread=False)

cursor = conn.cursor()

def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT 
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES cities(id)
    )
    ''')
    conn.commit()

def add_cities():
    cities = ['Warsaw', 'Cracow', 'Gdansk']
    for city in cities:
        cursor.execute('''
        INSERT INTO cities (city_name) VALUES (?)
        ''', (city, ))
    conn.commit()

def get_cities():
    cursor.execute('''
    SELECT * FROM cities
    ''')
    return cursor.fetchall()

def save_users(name, age, city_id):
    cursor.execute('''
    INSERT INTO users (name, age, city_id) VALUES (?, ?, ?)
    ''', (name, age, city_id))
    conn.commit()

#JOIN
# Warsaw
# 1 Asik 25 1


def get_users_with_cities():
    cursor.execute('''
    SELECT users.name, users.age,cities.city_name
    FROM users
    JOIN cities ON users.city_id = cities.id 
    ''')
    return cursor.fetchall()




create_tables()
# add_cities()
