import telebot
from telebot import types


bot = telebot.TeleBot('6044603159:AAF2-NYE_oOcCeTNLjf0wOlmRZMSIg8VwPc')

@bot.message_handler(commands=['start'])
def start(message):
    rmk = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    rmk.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
    msg = bot.send_message(message.from_user.id, 'Хотите узнать товары закончившиеся товары?', reply_markup=rmk)
    bot.register_next_step_handler(msg, get_course)

def get_course(message):
    if message.text == "Да":
        with open('/Users/egorkarinkin/PycharmProjects/Is_have_Wb_bot/products.csv', 'r', encoding='utf-8') as doc:
            bot.send_document(message.chat.id, doc)
    elif message.text == 'Нет':
        bot.send_message(message.from_user.id, 'До встречи!')


bot.infinity_polling(timeout=10, long_polling_timeout = 5)
