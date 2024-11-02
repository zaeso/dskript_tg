import os
import telebot
import cryptocode 


bot = telebot.TeleBot("") 

users = {} 

CONTENT_TYPES = ["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"]


def encrypt(arg, key): 
    encrypted = cryptocode.encrypt(arg, key) 
    return encrypted

def decrypt(arg, key): 
    decrypted = cryptocode.decrypt(arg, key) 
    if decrypted is False: 
        decrypted = "Текущий ключ не подходит для дешифровки сообщения" 
    return decrypted

def check_users(message_chat_id, message_chat_username): 
    global users 
    if message_chat_id not in users: 
        with open('cipherbot_users.log', 'a') as f: 
            f.write(str(message_chat_username) + ":" + str(message_chat_id) + "\n") 
        value = [None, None, False, None]  
        users.update({message_chat_id: value})

def reset_values_start(message_chat_id): 
    value = [None, None, False, None]  
    users.update({message_chat_id: value})
 
@bot.message_handler(commands=["start", "старт"]) 
def start(m, res=False): 
    message_chat_id = m.chat.id 
    reset_values_start(message_chat_id) 
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True) 
    item1 = telebot.types.KeyboardButton("Шифровать") 
    item2 = telebot.types.KeyboardButton("Расшифровать") 
    item3 = telebot.types.KeyboardButton("Ключ") 
    item4 = telebot.types.KeyboardButton("Помощь") 
    markup.add(item1) 
    markup.add(item2) 
    markup.add(item3) 
    markup.add(item4) 
    bot.send_message(m.chat.id, "Привет!\nЯ бот, умеющий зашифровывать и расшифровывать сообщения по заданному ключу.\n" "Выберите ключ и режим работы бота с помощью меню", reply_markup=markup)


@bot.message_handler(content_types=["text"]) 
def handle_text(message): 
    global users 
    message_chat_id = message.chat.id 
    message_from_user_username = message.from_user.username 
    check_users(message_chat_id, message_from_user_username) 

    if message.text.strip() == "Ключ": 
        users[message_chat_id][2] = True 
        answer = "Введите ключ" 
    elif users[message_chat_id][2] is True: 
        users[message_chat_id][1] = message.text 
        answer = "Текущий ключ: " + users[message_chat_id][1] 
        users[message_chat_id][2] = False 
    elif message.text.strip() == "Шифровать": 
        if users[message_chat_id][1] is None: 
            answer = "Ключ не может быть пустым. Введите значение ключа с помощью меню" 
        else: 
            users[message_chat_id][0] = "encrypt"
            users[message_chat_id][3] = "encrypt"
            answer = "[Ключ: " + users[message_chat_id][1] + "] Введите сообщение для шифровки" 
    elif message.text.strip() == 'Расшифровать': 
        if users[message_chat_id][1] is None: 
            answer = "Ключ не может быть пустым. Введите значение ключа с помощью меню" 
        else: 
            users[message_chat_id][0] = "decrypt"
            users[message_chat_id][3] = "decrypt"
            answer = "[Ключ: " + users[message_chat_id][1] + "] Введите сообщение для дешифровки" 
    elif message.text.strip() == "Помощь": 
        answer = "ИНФО:\nБот шифрует/дешифрует сообщения по заданному ключу.\n" \
               "Введите ключ затем выберите режим работы бота: шифровать/расшифровать.\n" \
               "В качестве ключа можно использовать любое число, слово, набор символов или их сочетание.\n" \
               "Чтобы перезагрузить бота введите /start или /старт"
    elif users[message_chat_id][1] is not None and users[message_chat_id][0] is None: 
        answer = "Выберите режим работы бота с помощью меню"
    elif users[message_chat_id][0] == "encrypt": 
        answer = encrypt(message.text, users[message_chat_id][1]) 
        users[message_chat_id][0] = None  
    elif users[message_chat_id][0] == "decrypt": 
        answer = decrypt(message.text, users[message_chat_id][1]) 
        users[message_chat_id][0] = None  
    else: 
        answer = "Сначала выберите ключ и режим работы бота с помощью меню" 

  
    bot.send_message(message.chat.id, answer) 

 
bot.polling(none_stop=True) 
