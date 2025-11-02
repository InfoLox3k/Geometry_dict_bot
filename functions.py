import telebot
from telebot import types
from token_data import *

# False - state of existance of message, 0 - message id, 0 - chat id,
message_sended = [[[False, 0, 0],  # Rectangle
                    [False, 0, 0],  # Circle
                   [False, 0, 0],  # Circle Ln
                  [False, 0, 0],  # Circle Ln H
                  [False, 0, 0],  # Circle Ln Ks
                   [False, 0, 0],  # Circle OK
                    [False, 0, 0],  # Corner
                    [False, 0, 0],  # Corner PE
                    [False, 0, 0],  # Straight
                    [False, 0, 0],  # Triangle
                    [False, 0, 0],  # Triangle PR
                    [False, 0, 0],  # Triangle OS
                    [False, 0, 0]  # Triangle TY
                  ]]

# список с id пользователей
ids_list = [5278854769]

# индексация нужного массива в message_sended
list_it = {"Rectangle": 0,
           "Circle": 1,
           "Circle Ln": 2,
           "Circle Ln H": 3,
           "Circle Ln Ks": 4,
           "Circle OK": 5,
           "Corner": 6,
           "Corner PE": 7,
           "Straight": 8,
           "Triangle": 9,
           "Triangle PR": 10,
           "Triangle OS": 11,
           "Triangle TY": 12
           }


bot = telebot.TeleBot(general_token)

# создание клавиатуры в сообщениях
def inline_keyboard(text_and_data_list, end_text, call_chat_id, msg):
    keyboard = types.InlineKeyboardMarkup()

    buttons_list = []

    for i in range(len(text_and_data_list)):
        buttons_list.append(types.InlineKeyboardButton(text=text_and_data_list[i][0], callback_data=text_and_data_list[i][1]))

    keyboard.add(*buttons_list)

    if msg != "only start" and msg != "":
        bot.send_message(call_chat_id, msg)

    bot.send_message(call_chat_id, text=end_text, reply_markup=keyboard)

# сброс данных о сообщениях одного пользователя
def list_clear(message):
    global message_sended, list_it, ids_list
    user_id = message.chat.id

    print(message_sended)
    print(ids_list)

    if user_id in ids_list:
        id_index = ids_list.index(user_id)
        del ids_list[id_index]
        del message_sended[id_index]

    print(message_sended)
    print(ids_list)

def look_nice(text):
    def output():
        print("------------------------------",
              text,
              "------------------------------")
    return output()

# проверка, есть ли отправленные сообщения
def check_message(chat_id):
    # если пользователь есть в системе
    if chat_id in ids_list:
        look_nice("YEAH")
        chat_info = ids_list.index(chat_id)
    else:
        # если нет, то создаём такой элемент
        message_sended.append([[False, 0, 0],  # Rectangle
                               [False, 0, 0],  # Circle
                               [False, 0, 0],  # Corner
                               [False, 0, 0],  # Corner PE
                               [False, 0, 0],  # Straight
                               [False, 0, 0],  # Triangle
                               [False, 0, 0],  # Triangle PR
                               [False, 0, 0],  # Triangle OS
                               [False, 0, 0],  # Triangle TY
                              ])
        ids_list.append(chat_id)
        chat_info = ids_list.index(chat_id)
    return chat_info

# отправка и изменение сообщений
def message_layer(call, new_text, info_type, picture=''):
    global message_sended, ids_list

    if picture != '':
        with open(picture, 'rb') as pic:
            sender(call, new_text, info_type, pic)
    else:
        sender(call, new_text, info_type, picture)

def sender(call, new_text, info_type, pic):
    global message_sended, ids_list

    chat_id = call.message.chat.id

    chat_info = check_message(chat_id)

    type_list = message_sended[chat_info][list_it[info_type]]
    print(type_list)

    if type_list[0] == False and type_list[1] == 0:
        if pic == '':
            try:
                bot_message = bot.send_message(call.message.chat.id, text=new_text, parse_mode="Markdown")
            except:
                bot.delete_message(chat_id=call.message.chat.id, message_id=type_list[1])
                bot_message = bot.send_message(call.message.chat.id, text=new_text, parse_mode="Markdown")
                type_list[1] = bot_message.message_id
                type_list[2] = call.message.chat.id
        else:
            bot_message = bot.send_photo(call.message.chat.id, photo=pic, caption=new_text, parse_mode="Markdown")
        type_list[0] = True
        type_list[1] = bot_message.message_id
        type_list[2] = call.message.chat.id
        message_sended[chat_info][list_it[info_type]] = type_list

    elif type_list[0] == True or type_list[1] != 0:
        if pic == '':
            try:
                bot.edit_message_text(text=new_text, chat_id=call.message.chat.id, message_id=type_list[1], parse_mode="Markdown")
            except:
                bot.delete_message(chat_id=call.message.chat.id, message_id=type_list[1])
                bot_message = bot.send_message(text=new_text, chat_id=call.message.chat.id, parse_mode="Markdown")
                type_list[1] = bot_message.message_id
                type_list[2] = call.message.chat.id
        else:
            bot.delete_message(chat_id=call.message.chat.id, message_id=type_list[1])
            bot_message = bot.send_photo(call.message.chat.id, photo=pic, caption=new_text, parse_mode="Markdown")
            type_list[1] = bot_message.message_id
            type_list[2] = call.message.chat.id
        type_list[0] = False
        message_sended[chat_info][list_it[info_type]] = type_list

    print(f"chat_info: {chat_info}")
    print(f"info_type: {info_type}")
    print(f"chat_id_state: {chat_id in ids_list}")
    print(f"ids_list: {ids_list}")
    print(f"chat_states: {message_sended[chat_info]}")
