import telebot
import random
from telebot import types
import csv 

bot = telebot.TeleBot('Your_bot_token')

button_press_count = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    #add markup
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item = types.KeyboardButton("Randomize 🔢")
    markup.add(item)
    bot.reply_to(message, "Hello! I can generate a random number from 1 to 25. Just use the keyboard button.", reply_markup=markup)

#main randomize button
@bot.message_handler(regexp="Randomize 🔢")
def contact_handler(message):
    #parsing info
    user_id = message.chat.id
    username = message.from_user.username if message.from_user.username else "Not available"
    chat_title = message.chat.title if message.chat.title else "Not available"
    first_name = message.from_user.first_name if message.from_user.first_name else "Not available"
    last_name = message.from_user.last_name if message.from_user.last_name else "Not available"
    chat_type = message.chat.type if message.chat.type else "Unknown"

    #information being recorded
    header = ["Chat ID", "Username", "Chat Title", "First Name", "Last Name", "Chat Type"]
    data_rows = [user_id, username, chat_title, first_name, last_name, chat_type]

    #write to csv file
    with open('User_info.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            
            file.seek(0, 2)
            file_empty = file.tell() == 0
            
            if file_empty:
                writer.writerow(header)
            
            writer.writerow(data_rows)

    #count number of click
    if user_id not in button_press_count:
        button_press_count[user_id] = 0

    if button_press_count[user_id] == 0:
        keyboard = types.InlineKeyboardMarkup()
        followers = types.InlineKeyboardButton('Generate random number💯', callback_data='followers')
        keyboard.add(followers)
        bot.send_message(user_id, "Press the button to generate random number from 1 to 25 ", reply_markup=keyboard)
    if button_press_count[user_id] == 1:
        keyboard = types.InlineKeyboardMarkup()
        followers = types.InlineKeyboardButton('Generate random number💯', callback_data='followers')
        keyboard.add(followers)
        bot.send_message(user_id, "Press the button to generate random number from 1 to 25 ", reply_markup=keyboard)
    if button_press_count[user_id] > 1:
        keyboard = types.InlineKeyboardMarkup()
        followers = types.InlineKeyboardButton('Generate random number💯', callback_data='followers')
        keyboard.add(followers)
        bot.send_message(user_id, "Press the button to generate random number from 1 to 25 ", reply_markup=keyboard)

#call function for randomize button
@bot.callback_query_handler(func=lambda call: True)
def handle_button_response(call):
    random_number = random.randint(1, 25)
    user_id = call.from_user.id

    if call.data == 'followers':
        try:
            if user_id not in button_press_count:
                button_press_count[user_id] = 0

            if button_press_count[user_id] == 0:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Your random number is: {random_number} \n\n<b>Click button one more time if you want another number 🔢</b>", parse_mode='html')
                button_press_count[user_id] += 1
            elif button_press_count[user_id] == 1:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Your random number is: 20\n\n<b>Click button one more time if you want another number 🔢</b>", parse_mode='html')
                button_press_count[user_id] += 1
            elif button_press_count[user_id] > 1:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Your random number is: {random_number}\n\n<b>Click button one more time if you want another number 🔢</b>", parse_mode='html')
        except:
            ...

bot.polling()
