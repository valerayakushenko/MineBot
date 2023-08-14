import telebot

from sql_def import *
from telebot import types
from dotenv import load_dotenv

if not os.path.exists('.env'):
    with open('.env', 'w') as env_file:
        env_file.write(f'token={input("Write your telegram api token: ")}')

load_dotenv()
token = os.getenv('token')
print(f'Telegram connected: {token}')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user = message.from_user
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🤖 My bots')
    btn2 = types.KeyboardButton('ℹ️ Info')
    markup.add(btn1, btn2)
    new_user(user.id, user.username)
    bot.send_message(message.chat.id, f'Hello, {user.first_name}!', reply_markup=markup)

@bot.message_handler(commands=['menu'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🤖 My bots')
    btn2 = types.KeyboardButton('ℹ️ Info')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "It's here:", reply_markup=markup)

@bot.message_handler()
def handle_start(message):
    user = message.from_user

    if message.text == '🤖 My bots':
        if check_count_bots(user.id) > 0:
            keyboard = types.InlineKeyboardMarkup(row_width=1)

            for i in range(check_count_bots(user.id)):
                btn1 = types.InlineKeyboardButton(f'{select_names(user.id)[i]}', callback_data=f'bot_{select_names(user.id)[i]}')
                keyboard.add(btn1)
            
            btn2 = types.InlineKeyboardButton('➕ New MineBot', callback_data='new_bot')
            keyboard.add(btn2)

            bot.send_message(message.chat.id, 'Choose a MineBot from the list below:',reply_markup=keyboard)
        else:
            btn1 = types.InlineKeyboardButton('➕ New MineBot', callback_data='new_bot')
            keyboard = types.InlineKeyboardMarkup()
            
            keyboard.add(btn1)
            bot.send_message(message.chat.id, 'You have currently no MineBots.',reply_markup=keyboard)
        return

    if check_task(user.id) == 'new_bot_1':
        if check_exist_names(user.id, message.text) == 0:
            new_bot_1(user.id, message.text)
            bot.send_message(message.chat.id, "Good. Now let's choose a username for your MineBot.")
            return
        else:
            bot.send_message(message.chat.id, 'Sorry, but you already have a bot with that name. Please write another.')
    
    if check_task(user.id) == 'new_bot_2':
        new_bot_2(user.id, message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('😔 No')
        btn2 = types.KeyboardButton('😄 Yes')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Alright, is this a licensed minecraft account?', reply_markup=markup)
        return

    if check_task(user.id) == 'new_bot_3' and message.text == '😄 Yes':
        new_bot_3_1(user.id)
        bot.send_message(message.chat.id, 'Great! Now send me the password for this account.', reply_markup=types.ReplyKeyboardRemove())
        return
    
    if check_task(user.id) == 'new_bot_3' and message.text == '😔 No':
        new_bot_3_2(user.id)
        bot.send_message(message.chat.id, "It's ok, now write me the ip address of the server.", reply_markup=types.ReplyKeyboardRemove())
        return
    
    if check_task(user.id) == 'new_bot_4':
        new_bot_4(user.id, message.text)
        bot.send_message(message.chat.id, "It's ok, now write me the ip address of the server.")
        return
    
    if check_task(user.id) == 'new_bot_5':
        new_bot_5(user.id, message.text)
        bot.send_message(message.chat.id, 'Nice! Now send me the server port.')
        return
    
    if check_task(user.id) == 'new_bot_6':
        new_bot_6(user.id, message.text)
        bot.send_message(message.chat.id, 'Ok, send me the server version.')
        return
    
    if check_task(user.id) == 'new_bot_end':
        new_bot_end(user.id, message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🤖 My bots')
        btn2 = types.KeyboardButton('ℹ️ Info')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "Great, we've added a new bot!", reply_markup=markup)
        return
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_'))
def callback_handler(call):
    user = call.from_user
    update_bot_data(user.id, call.data[5:])

@bot.callback_query_handler(func=lambda call: call.data.startswith('bot_'))
def callback_handler(call):
    user = call.from_user
    bot_name = call.data[4:]

    set_current_bot(user.id, bot_name)
    keyboard = types.InlineKeyboardMarkup(row_width=2) 

    btn1 = types.InlineKeyboardButton('MineBot Control', callback_data='task_bot_control')
    keyboard.add(btn1)
    btn2 = types.InlineKeyboardButton('MineBot Info', callback_data='task_bot_info')
    btn3 = types.InlineKeyboardButton('MineBot Status', callback_data='task_bot_status')
    btn4 = types.InlineKeyboardButton('Edit MineBot', callback_data='task_bot_edit')
    btn5 = types.InlineKeyboardButton('Delete MineBot', callback_data='task_bot_delete')
    keyboard.row(btn2, btn3)
    keyboard.row(btn4, btn5)

    btn6 = types.InlineKeyboardButton('<< Back to MineBots List', callback_data='task_bot_back')
    keyboard.add(btn6)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Here it is: {call.data[4:]}\nWhat do you want to do with the bot?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'new_bot':
        user = call.from_user
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        btn1 = types.InlineKeyboardButton('<< Cancel', callback_data='new_bot_cancel')
        keyboard.row(btn1)
        
        new_bot_0(user.id)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Alright, a new MineBot. How are we going to call it? Please choose a friendly name for your MineBot.', reply_markup=keyboard)
        return
    
    if call.data == 'new_bot_cancel':
        user = call.from_user
        delete_bot(user.id, check_currently_bot(user.id))
        update_user_data(user.id, 'current_task', '0')
        update_user_data(user.id, 'current_bot', '0')
        if check_count_bots(user.id) > 0:
            keyboard = types.InlineKeyboardMarkup(row_width=1)

            for i in range(check_count_bots(user.id)):
                btn1 = types.InlineKeyboardButton(f'{select_names(user.id)[i]}', callback_data=f'bot_{select_names(user.id)[i]}')
                keyboard.add(btn1)
            
            btn2 = types.InlineKeyboardButton('➕ New MineBot', callback_data='new_bot')
            keyboard.add(btn2)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Choose a MineBot from the list below:', reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup()
            
            btn1 = types.InlineKeyboardButton('➕ New MineBot', callback_data='new_bot')
            keyboard.add(btn1)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='You have currently no MineBots.', reply_markup=keyboard)
        return

    if call.data == 'task_bot_back':
        user = call.from_user
        if check_count_bots(user.id) > 0:
            keyboard = types.InlineKeyboardMarkup(row_width=1)

            for i in range(check_count_bots(user.id)):
                btn1 = types.InlineKeyboardButton(f'{select_names(user.id)[i]}', callback_data=f'bot_{select_names(user.id)[i]}')
                keyboard.add(btn1)
            
            btn2 = types.InlineKeyboardButton('➕ New MineBot', callback_data='new_bot')
            keyboard.add(btn2)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Choose a MineBot from the list below:',reply_markup=keyboard)
        else:
            btn1 = types.InlineKeyboardButton('➕ New MineBot', callback_data='new_bot')
            keyboard = types.InlineKeyboardMarkup()
            
            keyboard.add(btn1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='You have currently no MineBots.', reply_markup=keyboard)
        return
    
    if call.data == 'task_bot_info':
        user = call.from_user
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        
        bot_id = check_currently_bot(user.id)
        bot_info = select_bot_info(user.id, bot_id)

        if bot_info[4] == '0':
            btn1 = types.InlineKeyboardButton('<< Back to MineBot Panel', callback_data=f'bot_{bot_info[2]}')
            keyboard.add(btn1)

            text = f'''Here it is: {bot_info[2]}

    Friendly name: {bot_info[2]}
    Username: {bot_info[3]}
    Server ip: {bot_info[5]}
    Server port: {bot_info[6]}
    Server version: {bot_info[7]}
    '''
        else:
            btn1 = types.InlineKeyboardButton('Show password', callback_data='task_bot_info_password')
            btn2 = types.InlineKeyboardButton('<< Back to MineBot Panel', callback_data=f'bot_{bot_info[2]}')
            keyboard.add(btn1, btn2)

            text = f'''Here it is: {bot_info[2]}

    Friendly name: {bot_info[2]}
    Username: {bot_info[3]}
    Password: {'*' * len(bot_info[4])}
    Server ip: {bot_info[5]}
    Server port: {bot_info[6]}
    Server version: {bot_info[7]}
    '''
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=keyboard)
        return
    
    if call.data == 'task_bot_info_password':
        user = call.from_user
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        
        bot_id = check_currently_bot(user.id)
        bot_info = select_bot_info(user.id, bot_id)

        btn1 = types.InlineKeyboardButton('Hide password', callback_data=f'task_bot_info')
        btn2 = types.InlineKeyboardButton('<< Back to MineBot Panel', callback_data=f'bot_{bot_info[2]}')
        keyboard.add(btn1, btn2)

        text = f'''Here it is: {bot_info[2]}

    Friendly name: {bot_info[2]}
    Username: {bot_info[3]}
    Password: {bot_info[4]}
    Server ip: {bot_info[5]}
    Server port: {bot_info[6]}
    Server version: {bot_info[7]}
    '''
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=keyboard)
        return
    
    if call.data == 'task_bot_status':
        user = call.from_user
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        bot_id = check_currently_bot(user.id)
        bot_info = select_bot_info(user.id, bot_id)

        btn1 = types.InlineKeyboardButton('<< Back to MineBot Panel', callback_data=f'bot_{bot_info[2]}')
        keyboard.add(btn1)

        text = f'''Here it is: {bot_info[2]}

    MineBot Online:
    Server Online:
    '''

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=keyboard)
        return
    
    if call.data == 'task_bot_delete':
        user = call.from_user
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        bot_id = check_currently_bot(user.id)
        bot_info = select_bot_info(user.id, bot_id)

        btn1 = types.InlineKeyboardButton('❌ No', callback_data=f'bot_{bot_info[2]}')
        btn2 = types.InlineKeyboardButton('✅ Yes', callback_data='delete_bot')
        keyboard.row(btn1, btn2)

        text = f'Are you sure to delete bot: {bot_info[2]}'

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=keyboard)
        return
    
    if call.data == 'delete_bot':
        user = call.from_user
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        delete_bot(user.id, check_currently_bot(user.id))
        update_user_data(user.id, 'current_task', '0')
        update_user_data(user.id, 'current_bot', '0')
        
        bot_id = check_currently_bot(user.id)
        bot_info = select_bot_info(user.id, bot_id)

        btn1 = types.InlineKeyboardButton('<< Back', callback_data=f'task_bot_back')
        keyboard.add(btn1)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Done ✅!', reply_markup=keyboard)
        return
    
    if call.data == 'task_bot_edit':
        user = call.from_user
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        bot_id = check_currently_bot(user.id)
        bot_info = select_bot_info(user.id, bot_id)

        btn1 = types.InlineKeyboardButton('Friendly name', callback_data=f'edit_bot_name')
        btn2 = types.InlineKeyboardButton('Username', callback_data=f'edit_bot_username')
        btn3 = types.InlineKeyboardButton('Password', callback_data=f'edit_bot_password')
        btn4 = types.InlineKeyboardButton('Server IP', callback_data=f'edit_server_ip')
        btn5 = types.InlineKeyboardButton('Server Port', callback_data=f'edit_server_port')
        btn5 = types.InlineKeyboardButton('Server Version', callback_data=f'edit_server_version')
        btn6 = types.InlineKeyboardButton('<< Back to MineBot Panel', callback_data=f'bot_{bot_info[2]}')
        keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Here it is: {bot_info[2]}\n\nEdit:', reply_markup=keyboard)
        return
        
bot.polling(none_stop=True)
