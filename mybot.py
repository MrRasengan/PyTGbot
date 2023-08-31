import telebot
import webbrowser
from telebot import types

bot = telebot.TeleBot('6652814884:AAF0LSZEZjmGEZZmGQPVRVCA9oL0ndNJSWU')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Удалить фото')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Изменить текст')
    btn3 = types.KeyboardButton('Перейти на сайт')
    markup.row(btn2, btn3)
    file = open('./photo.jpg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Website open')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Фото удалено')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://gb.ru')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}') 

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Информация</b> <u>по</u> <em>боту</em>', parse_mode='html') 

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    btn3 = types.InlineKeyboardButton('Перейти на сайт', url='https://gb.ru')
    markup.row(btn2, btn3)
    bot.reply_to(message, 'Отличное фото!', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data  == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id -1)
    elif callback.data  == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}') 
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.polling(none_stop=True)