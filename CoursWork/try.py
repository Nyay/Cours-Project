import sqlite3

def step_1():
    TABLE_NAME = input('Введите названия таблицы: ')
    try:
        conn = sqlite3.connect('Cours_Base.db', timeout=10)
        CREATE_COMAND ='CREATE TABLE ' + TABLE_NAME + ' (QUESTION_ID   INTEGER PRIMARY KEY   NOT NULL, QUESTION_TEXT   TEXT   NOT NULL)'
        conn.execute(CREATE_COMAND)
        print ('Таблица ' + TABLE_NAME + ' создана.')
        conn.close()
    except:
        print('Таблица уже существует.')

def step_2():
    #step_1()
    TABLE_NAME = input('Введите название нужной таблицы: ')
    ID_NAME = input('Введите ID нужного вопроса: ')
    conn = sqlite3.connect('Cours_Base.db')
    cursor = conn.cursor()
    print('База успешно загружена.')
    FIND_COMAND = 'SELECT QUESTION_TEXT FROM ' + TABLE_NAME + ' WHERE QUESTION_ID = ' + ID_NAME
    cursor.execute(FIND_COMAND)
    data = cursor.fetchall()
    print(data)
    conn.close()

step_2()