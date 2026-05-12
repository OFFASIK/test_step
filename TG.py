import telebot
import os
from dotenv import load_dotenv
from Db import get_cities, get_users_with_cities, save_users
load_dotenv()

token = os.getenv("TOKEN")
admin_id = os.getenv("ADMIN")
bot = telebot.TeleBot(token)

user_state={}

@bot.message_handler(commands=['users'])
def command_users(message):
    if message.chat.id == admin_id:
        users = get_users_with_cities()
        result = 'Список пользователей: \n'
        for user in users:
            result += f'{user[0]} {user[1]} - {user[2]}\n'
        bot.send_message(message.chat.id, result)
        print(result)
    else:
        bot.send_message(message.chat.id,'Отказано в доступе')



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Как тебя зовут?")
    user_state[message.chat.id] = {'step': 'name'}

@bot.message_handler(content_types=['text'])
def handler(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)

    if not state:
        return

    if state['step'] == "name":
        state["name"] = message.text
        state["step"] = "age"
        bot.send_message(message.chat.id, "Укажите возраст")

    elif state['step'] == "age":
        state["age"] = message.text
        state["step"] = "city"

        text = "выберите Город: \n"

        cities = get_cities()
        for city in cities:
            text += f'{city[0]} - {city[1]}\n'

        bot.send_message(chat_id,text)

    elif state["step"] == "city":
        city_id = int(message.text)


        save_users(state["name"], state["age"], city_id)


        bot.send_message(chat_id, "Сохранено")
        print(user_state[chat_id])
        user_state[chat_id] = None







if __name__ == '__main__':
    bot.polling(none_stop=True)


