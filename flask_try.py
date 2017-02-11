from flask import Flask
from flask import url_for, render_template, request
import sqlite3
import os
import random
import csv


app = Flask(__name__)


def add_info_to_db(db, table, where, what):
    conn = sqlite3.connect(str(db))
    CMD = 'INSERT INTO ' + table + ' (' + where + ') VALUES (' + what + ');'
    conn.execute(CMD)
    conn.commit()
    conn.close()

def open_file_read(NAME):
    OPENING_FILE = open(NAME, 'r', encoding='UTF-8')
    TEXT = OPENING_FILE.read()
    OPENING_FILE.close()
    return TEXT

# Возвращает текст файла

def open_file_line(NAME):
    OPENING_FILE = open(NAME, 'r', encoding='UTF-8')
    TEXT = OPENING_FILE.readlines()
    OPENING_FILE.close()
    return TEXT

# Возвращает текст файла (линейно)

def download_txt_files():
    TXT_FILES = []
    ALL_FILES = os.listdir()
    for ELEMENT in ALL_FILES:
        if ELEMENT.endswith('.txt'):
            TXT_FILES.append(ELEMENT)
    return TXT_FILES

# Возвращает список файлов в дрк

def create_table_qs(table_name):
    try:
        conn = sqlite3.connect('QS_And_Forms_DB.db')
        COMAND = 'CREATE TABLE ' + table_name + ' (QUESTION_ID   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, QUESTION_TEXT   TEXT   NOT NULL, QUESTION_BLOCK   TEXT   NOT NULL)'
        conn.execute(COMAND)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print('        table exist         ')

# Создание таблиц для вопросов

def create_table_forms(table_name):
    try:
        conn = sqlite3.connect('QS_And_Forms_DB.db')
        COMAND = 'CREATE TABLE ' + table_name + ' (QUESTION_ID   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, QUESTION_TEXT   TEXT   NOT NULL,)'
        conn.execute(COMAND)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print('        table exist         ')

# Создание таблицы для форм

def insert_task_qs(QT, TABLE_NAME, BLOCK_NAME):
    for element in QT:
        conn = sqlite3.connect('QS_And_Forms_DB.db')
        COMMAND = 'INSERT INTO ' + TABLE_NAME + ' (QUESTION_TEXT, QUESTION_BLOCK) VALUES (' + "'" + element + "','" + BLOCK_NAME + "'" +');'
        conn.execute(COMMAND)
        conn.commit()
        conn.close()

# Добавление вопросов в таблицу

def get_tables_names():
    Final_list = []
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    cursor = conn.cursor()
    COMAND = 'SELECT NAME FROM sqlite_master WHERE type=' + "'" + 'table' + "'" + 'ORDER BY name;'
    cursor.execute(COMAND)
    LIST_OF_NAMES = cursor.fetchall()
    for element in LIST_OF_NAMES:
        for el in element:
            Final_list.append(el)
    conn.close()
    return Final_list

# Достаем название таблиц(Форм из DB)

def get_form(TABLE_NAME):
    Final_list = []
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    cursor = conn.cursor()
    COMAND = 'SELECT QUESTION_TEXT FROM ' + TABLE_NAME
    cursor.execute(COMAND)
    LIST_OF_NAMES = cursor.fetchall()
    for element in LIST_OF_NAMES:
        for el in element:
            Final_list.append(el)
    conn.close()
    return Final_list

# Достаем вопросы из формы

def get_id(TABLE_NAME):
    Final_list = []
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    cursor = conn.cursor()
    COMAND = 'SELECT QUESTION_ID FROM ' + TABLE_NAME
    cursor.execute(COMAND)
    LIST_OF_NAMES = cursor.fetchall()
    for element in LIST_OF_NAMES:
        for el in element:
            Final_list.append(el)
    conn.close()
    return Final_list

# Достаем id вопросов из формы

def add_ans(El1, El2, El3):
    conn = sqlite3.connect('ANS_DB.db')
    try:
        COMAND = 'CREATE TABLE ALL_ANS (QS_ID   INTEGER NOT NULL , QS_TXT   TEXT   NOT NULL, ANS_TXT TEXT NOT NULL)'
        conn.execute(COMAND)
    except sqlite3.OperationalError:
        print('        table exist         ')
    COMAND = 'INSERT INTO ALL_ANS (QS_ID, QS_TXT, ANS_TXT) VALUES (' + "'" + str(El1) + "','" + str(El2) + "','" + str(El3) + "');"
    conn.execute(COMAND)
    conn.commit()
    conn.close()

# Добавление ответов в таблицу


def search_task(db, table, uprise):
    search_result = []
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    CMD = 'SELECT ' + str(uprise) + ' FROM ' + str(table)
    cursor.execute(CMD)
    search_taple = cursor.fetchall()
    for element in search_taple:
        for el in element:
            search_result.append(el)
    conn.close()
    return search_result

#

def search_task_where(db, table, uprise, what_in):
    search_result = []
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    CMD = 'SELECT * FROM ' + str(table) + ' WHERE ' + str(uprise) + ' = ' + str(what_in)
    cursor.execute(CMD)
    search_taple = cursor.fetchall()
    for element in search_taple:
        for el in element:
            search_result.append(el)
    print(search_result)
    conn.close()
    return search_result

#

def search_what_by_arg(what, db, table, wtf, arg):
    search_result = []
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    CMD = 'SELECT ' + str(what) + ' FROM ' + str(table) + ' WHERE ' + str(wtf) + ' = ' + "'" + str(arg) + "' ;"
    print(CMD)
    cursor.execute(CMD)
    search_taple = cursor.fetchall()
    for element in search_taple:
        for el in element:
            search_result.append(el)
    conn.close()
    return search_result

#

def export_to_csv(db):
    with sqlite3.connect(db) as connection:
        csvWriter = csv.writer(open("output.csv", "w"),  delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        c = connection.cursor()
        CMD = 'SELECT * FROM ALL_ANS'
        c.execute(CMD)
        rows = c.fetchall()
        csvWriter.writerow(['ID Вопроса', 'Текст вопроса', 'Ответ респодента', 'ID респодента'])
        csvWriter.writerows(rows)

# Экспорт результатов в CSV файл.


@app.route('/')
def main_page_task():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    return render_template('main.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4)


@app.route('/ch_wh_to_add')
def ch_wh_to_add():
    NAMES = download_txt_files()
    return render_template('ch_wh_to_add.html', NAMES = NAMES)


@app.route('/add_info')
def add_info():
    return render_template('add_info.html')


@app.route('/add_to_db')
def add_to_db():
    FILE_NAME = request.args['file_name']
    BLOCK_NAME = request.args['block_name']
    QUESTION_TEXT = open_file_read(FILE_NAME)
    QUESTION_TEXT = QUESTION_TEXT.split('\n')
    create_table_qs('List_of_qs_try')
    insert_task_qs(QUESTION_TEXT, 'List_of_qs_try', BLOCK_NAME)
    urls = {'Добавить еще один блок вопросов.': url_for('add_info'),
            }
    return render_template('add_to_db.html', urls=urls)


@app.route('/crt_form')
def crt_form():
    return render_template('crt_form.html')


@app.route('/crt_form_fnl')
def crt_form_fnl():
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    MAX_QS_MUN = request.args['amount']
    MAX_QS_MUN = int(MAX_QS_MUN)
    FORM_NAME = request.args['form_name']
    BLOCK_NAME = request.args['block_name']
    List_of_QS = []
    Comand = 'SELECT QUESTION_ID,QUESTION_TEXT FROM List_of_qs_try WHERE QUESTION_BLOCK = ' + "'" + str(BLOCK_NAME) + "'"
    cursor = conn.cursor()
    cursor.execute(Comand)
    group_of_items = cursor.fetchall()
    list_of_random_items = random.sample(group_of_items, MAX_QS_MUN)
    for word in list_of_random_items:
        List_of_QS.append(word[0])
    try:
        COMAND = 'CREATE TABLE ' + str(FORM_NAME) + ' (QUESTION_ID   INTEGER   NOT NULL, QUESTION_TEXT   TEXT   NOT NULL)'
        conn.execute(COMAND)
        conn.commit()
    except sqlite3.OperationalError:
        print('        table exist         ')
    for element in list_of_random_items:
        COMMAND_ADD = 'INSERT INTO ' + str(FORM_NAME) + ' (QUESTION_ID, QUESTION_TEXT) VALUES (' + "'" + str(element[0]) + "','" + str(element[1]) + "'" +');'
        conn.execute(COMMAND_ADD)
        conn.commit()
    return render_template('crt_form_fnl.html', list_of_random_items=list_of_random_items)


@app.route('/select_form')
def select_form():
    TABLES = get_tables_names()
    return render_template('cmp_form.html', TABLES=TABLES)


@app.route('/open_form')
def open_form():
    global NAME
    NAME = request.args['selected_form']
    List_Q = get_form(NAME)
    return render_template('open_form.html', List_Q=List_Q)


@app.route('/check_ans')
def check_ans():
    name1 = NAME
    print(name1)
    answers = []
    ids = get_id(name1)
    qs_text = get_form(name1)
    for element in qs_text:
        ans = request.args[element]
        answers.append(ans)
    for i in range(len(answers)):
        add_ans(ids[i], qs_text[i], answers[i])
    x = len(answers)
    return render_template('check_ans.html', qs_text=qs_text, answers=answers,x=x)


@app.route('/search_id')
def search_id():
    search_args = search_task('ANS_Db.db', 'cors_info', 'id')
    print(search_args)
    return render_template('search_id.html', info = search_args)


@app.route('/search_name')
def search_name():
    search_args = search_task('cors_info.db', 'cors_info', 'name')
    print(search_args)
    return render_template('search_name.html', info = search_args)


@app.route('/search_name_result')
def search_name_result():
    final_result = []
    name = request.args['name']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'name', name)
    for el in my_id:
        fin = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        final_result.append(fin)
    print(my_id)
    print(final_result)

@app.route('/search_year')
def search_year():
    search_args = search_task('cors_info.db', 'cors_info', 'year')
    print(search_args)
    return render_template('search_town.html', info = search_args)


@app.route('/search_year_result')
def search_year_result():
    year = request.args['year']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'year', year)
    for el in my_id:
        result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        print(result)
    print(my_id)

@app.route('/search_town')
def search_town():
    search_args = search_task('cors_info.db', 'cors_info', 'town')
    print(search_args)
    return render_template('search_town.html', info = search_args)


@app.route('/search_town_result')
def search_town_result():
    town = request.args['town']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'town', town)
    for el in my_id:
        result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        print(result)
    print(my_id)


@app.route('/search_gender')
def search_gender():
    search_args = search_task('cors_info.db', 'cors_info', 'gender')
    print(search_args)
    search_args = set(search_args)
    return render_template('search_gender.html', info = search_args)


@app.route('/search_gender_result')
def search_gender_result():
    gender = request.args['gender']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'gender', gender)
    for el in my_id:
        result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        print(result)
    print(my_id)


@app.route('/add_cors')
def add_cors():
    return render_template('add_cors.html')


@app.route('/add_cors_fin')
def add_cors_fin():
    name = request.args['name']
    year = request.args['year']
    gender = request.args['gender']
    town = request.args['town']
    raw1 = "'" + str(name) + "','" + str(year) + "','" + str(town) + "','" + str(gender) + "'"
    raw2 = 'name, year, town, gender'
    add_info_to_db('cors_info.db', 'cors_info', raw2, str(raw1))


@app.route('/convert_to_csv')
def convert_to_csv():
    export_to_csv('ANS_DB.db')
    render_template('')


if __name__ == '__main__':
    app.run(debug=True)