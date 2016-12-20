import sqlite3

def step_1():
    TABLE_NAME = input('Введите названия таблицы: ')
    try:
        conn = sqlite3.connect('Main_DB.db', timeout=10)
        CREATE_COMAND ='CREATE TABLE ' + TABLE_NAME + ' (QUESTION_ID   INTEGER PRIMARY KEY   NOT NULL, QUESTION_TEXT   TEXT   NOT NULL)'
        conn.execute(CREATE_COMAND)
        print ('Таблица ' + TABLE_NAME + ' создана.')
        conn.close()
    except:
        print('Таблица уже существует.')

def step_2():
    step_1()
    TABLE_NAME = input('Введите название нужной таблицы: ')
    conn = sqlite3.connect('Main_DB.db')
    print('База успешно загружена.')
    QUESTION_FILE = open('QTP.txt', 'r', encoding='UTF-8')
    QUESTION_TEXT = QUESTION_FILE.read()
    QUESTION_TEXT = QUESTION_TEXT.split('\n')
    for element in QUESTION_TEXT:
        COMMAND = 'INSERT INTO ' + TABLE_NAME + ' (QUESTION_TEXT) VALUES (' + "'" + element +  "'" + ');'
        conn.execute(COMMAND)
    conn.commit()
    print('Инфомация успешно загружена.')
    conn.close()

def step_3():
    TABLE_NAME = input('Введите название нужной таблицы: ')
    ID_NAME = input('Введите ID нужного вопроса: ')
    conn = sqlite3.connect('Main_DB.db')
    cursor = conn.cursor()
    print('База успешно загружена.')
    FIND_COMAND = 'SELECT QUESTION_TEXT FROM ' + TABLE_NAME + ' WHERE QUESTION_ID = ' + ID_NAME
    cursor.execute(FIND_COMAND)
    DATA = cursor.fetchall()
    print(DATA)
    conn.close()

step_2()
step_3()