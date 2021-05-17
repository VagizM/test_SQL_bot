import sqlite3
import os
import datetime

'''
Параметрыв БД
r_id          уникальное значение записи
r_user_id     автор записи
r_data        время создания записи   timestamp
r_text        текст
r_category     понадобиться позже!!!!!!!

Методы
creat_base()                return   T/F
add_record(user_id,text)    return   T/F id/F
get_record(id)              return   id,user_id,data,text
get_records(user_id)        return   [(id,user_name,data,text),(),()...]
del_record(id)              return   T/F

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT PRIMARY KEY,
   fname TEXT,
   lname TEXT,
   gender TEXT);
""")
conn.commit()

'''



def creat_base():
    if  (not os.path.exists('data.db')):        
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE user_db (r_id INTEGER PRIMARY KEY AUTOINCREMENT, r_user_id INTEGER, r_date TEXT, r_text TEXT)')
    # !!! проверить создание БД, корректнее проверять файл и БД а не только файл
        return True  
  
    
def add_record(user_id, text):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    datet = datetime.datetime.now() 
    cur.execute(f'INSERT INTO user_db (r_user_id, r_date, r_text) VALUES("{user_id}", "{datet}","{text}")')
    conn.commit() 
    cur.execute(f'SELECT * FROM user_db WHERE r_date = "{datet}"')
    result = cur.fetchall()    
    if result == []:
        return False
    else:
        return True

def get_records(user_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM user_db WHERE r_user_id = "{user_id}"')
    #  !!! Проверка данных если их нет то вернуть False
    result = cur.fetchall()
    if result == []:
        return False
    else:
        return result

def get_record(r_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM user_db WHERE r_id = "{r_id}"')
    #  !!! Проверка данных если их нет то вернуть False
    result = cur.fetchone()
    if result == []:
        return False
    else:
        return result


def del_record(r_id):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM user_db WHERE r_id = "{r_id}"')
    if cur.fetchall() == []:
        return False
    else:
        cur.execute(f'DELETE FROM user_db WHERE r_id = "{r_id}";')
        conn.commit()
        #  !!! Проверка данных если их нет то вернуть False
        return True


if __name__ == "__main__":
    creat_base()
    print(add_record("50","test rec22"))
    print(get_records("50"))
    print(get_record("50"))
   # print(del_record("6"))