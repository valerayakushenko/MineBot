import os
import sqlite3

if not os.path.exists('data.db'):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()

    cursor.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        tele_id INTEGER,
        username TEXT,
        current_task TEXT,
        current_bot TEXT
    )""")

    cursor.execute("""CREATE TABLE bots (
        id INTEGER PRIMARY KEY,
        tele_id TEXT,
        bot_name TEXT,
        bot_username TEXT,
        bot_password TEXT,
        server_ip TEXT,
        server_port TEXT,
        server_version TEXT
    )""")

    database.commit()
    database.close()

    print('Database created.')
else:
    print('Database connected.')


def new_user(tele_id, username):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM users WHERE tele_id = {tele_id}")
    exist = cursor.fetchone()[0]
    if exist == 0:
        cursor.execute(f"INSERT INTO users(tele_id, username, current_task, current_bot) VALUES ('{tele_id}', '{username}', '0', '0')")
    else:
        cursor.execute(f"UPDATE users SET current_task = '0' WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def check_task(tele_id):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT current_task FROM users WHERE tele_id = {tele_id}")
    result = cursor.fetchone()[0]
    database.close()
    return result

def check_currently_bot(tele_id):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT current_bot FROM users WHERE tele_id = {tele_id}")
    result = cursor.fetchone()[0]
    database.close()
    return result

def check_count_bots(tele_id):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM bots WHERE tele_id = {tele_id}")
    result = cursor.fetchone()[0]
    database.close()
    return result

def check_exist_names(tele_id, bot_name):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM bots WHERE tele_id = {tele_id} AND bot_name = '{bot_name}'")
    result = cursor.fetchone()[0]
    database.close()
    return result

def select_names(tele_id):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT bot_name FROM bots WHERE tele_id = {tele_id}")
    column_values_list = cursor.fetchall()
    result = [row[0] for row in column_values_list]
    database.close()
    return result

def select_bot_info(tele_id, bot_id):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT * FROM bots WHERE tele_id = {tele_id} AND id = {bot_id}")
    result = cursor.fetchone()
    database.close()
    return result

def new_bot_0(tele_id):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO bots(tele_id, bot_name, bot_username, bot_password, server_ip, server_port, server_version) VALUES ('{tele_id}', '0', '0', '0', '0', '0', '0')")
    cursor.execute(f"UPDATE users SET current_task = 'new_bot_1' WHERE tele_id = {tele_id}")
    cursor.execute(f"SELECT MAX(id) FROM bots WHERE tele_id = {tele_id}")
    result = cursor.fetchone()[0]
    cursor.execute(f"UPDATE users SET current_bot = {result} WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def new_bot_1(tele_id, bot_name):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT current_bot FROM users WHERE tele_id = {tele_id}")
    current_bot = cursor.fetchone()[0]
    cursor.execute(f"UPDATE bots SET bot_name = '{bot_name}' WHERE tele_id = {tele_id} AND id = {current_bot}")
    cursor.execute(f"UPDATE users SET current_task = 'new_bot_2' WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def new_bot_2(tele_id, bot_username):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT current_bot FROM users WHERE tele_id = {tele_id}")
    current_bot = cursor.fetchone()[0]
    cursor.execute(f"UPDATE bots SET bot_username = '{bot_username}' WHERE tele_id = {tele_id} AND id = {current_bot}")
    cursor.execute(f"UPDATE users SET current_task = 'new_bot_3' WHERE tele_id = {tele_id}")
    database.commit()
    database.close()
    
def new_bot_3_1(tele_id):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"UPDATE users SET current_task = 'new_bot_4' WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def new_bot_3_2(tele_id):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"UPDATE users SET current_task = 'new_bot_5' WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def new_bot_4(tele_id, bot_password):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT current_bot FROM users WHERE tele_id = {tele_id}")
    current_bot = cursor.fetchone()[0]
    cursor.execute(f"UPDATE bots SET bot_password = '{bot_password}' WHERE tele_id = {tele_id} AND id = {current_bot}")
    cursor.execute(f"UPDATE users SET current_task = 'new_bot_5' WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def new_bot_5(tele_id, server_ip):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT current_bot FROM users WHERE tele_id = {tele_id}")
    current_bot = cursor.fetchone()[0]
    cursor.execute(f"UPDATE bots SET server_ip = '{server_ip}' WHERE tele_id = {tele_id} AND id = {current_bot}")
    cursor.execute(f"UPDATE users SET current_task = 'new_bot_6' WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def new_bot_6(tele_id, server_port):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT current_bot FROM users WHERE tele_id = {tele_id}")
    current_bot = cursor.fetchone()[0]
    cursor.execute(f"UPDATE bots SET server_port = '{server_port}' WHERE tele_id = {tele_id} AND id = {current_bot}")
    cursor.execute(f"UPDATE users SET current_task = 'new_bot_end' WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def new_bot_end(tele_id, server_version):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT current_bot FROM users WHERE tele_id = {tele_id}")
    current_bot = cursor.fetchone()[0]
    cursor.execute(f"UPDATE bots SET server_version = '{server_version}' WHERE tele_id = {tele_id} AND id = {current_bot}")
    cursor.execute(f"UPDATE users SET current_task = '0' WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def set_current_bot(tele_id, bot_name):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT id FROM bots WHERE tele_id = {tele_id} AND bot_name = '{bot_name}'")
    bot_id = cursor.fetchone()[0]
    cursor.execute(f"UPDATE users SET current_bot = {bot_id} WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def update_user_data(tele_id, column, data):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"UPDATE users SET {column} = '{data}' WHERE tele_id = {tele_id}")
    database.commit()
    database.close()

def delete_bot(tele_id, bot_id):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"DELETE FROM bots WHERE tele_id = {tele_id} AND id = {bot_id}")
    database.commit()
    database.close()

def update_bot_data(tele_id, column, data):
    database = sqlite3.connect('data.db', check_same_thread=False)
    cursor = database.cursor()
    cursor.execute(f"SELECT current_bot FROM users WHERE tele_id = {tele_id}")
    current_bot = cursor.fetchone()[0]
    cursor.execute(f"UPDATE bots SET {column} = '{data}' WHERE tele_id = {tele_id} AND id = {current_bot}")
    database.commit()
    database.close()