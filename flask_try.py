from flask import Flask, session
from flask import url_for, render_template, request
import sqlite3
import os
import random
import csv
import json
import conf
import re
import os


app = Flask(__name__)
key = os.urandom(24)
app.secret_key = key
#print(key)


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


def insert_task_qs_2(QT, TABLE_NAME, BLOCK_NAME):
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    COMMAND = 'INSERT INTO ' + TABLE_NAME + ' (QUESTION_TEXT, QUESTION_BLOCK) VALUES (' + "'" + QT + "','" + BLOCK_NAME + "'" +');'
    conn.execute(COMMAND)
    conn.commit()
    conn.close()


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

def get_column(data_base, column, table_name):
    final_list = []
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cmd = 'SELECT ' + column + ' FROM ' + table_name
    cursor.execute(cmd)
    list_of_names = cursor.fetchall()
    for element in list_of_names:
        for el in element:
            final_list.append(el)
    conn.close()
    return final_list


def get_block_name(TABLE_NAME):
    Final_list = []
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    cursor = conn.cursor()
    COMAND = 'SELECT QUESTION_BLOCK FROM ' + TABLE_NAME
    cursor.execute(COMAND)
    LIST_OF_NAMES = cursor.fetchall()
    for element in LIST_OF_NAMES:
        for el in element:
            Final_list.append(el)
    conn.close()
    return set(Final_list)


def get_block_qs_amount(TABLE_NAME, arg):
    QS_list = []
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    cursor = conn.cursor()
    COMAND = 'SELECT QUESTION_TEXT FROM ' + str(TABLE_NAME) + " WHERE QUESTION_BLOCK = '" + str(arg) + "' ;"
    cursor.execute(COMAND)
    LIST_OF_NAMES = cursor.fetchall()
    for element in LIST_OF_NAMES:
        for el in element:
            QS_list.append(el)
    conn.close()
    return len(QS_list)


def add_ans_fnc(qs_id, qs_txt, ans_txt, cors_txt):
    conn = sqlite3.connect('ANS_DB.db')
    try:
        cmd = 'CREATE TABLE ALL_ANS (QS_ID   INTEGER NOT NULL , QS_TXT   TEXT   NOT NULL, ANS_TXT TEXT NOT NULL)'
        conn.execute(cmd)
    except sqlite3.OperationalError:
        print('        table exist         ')
    cmd = "INSERT INTO ALL_ANS (QS_ID, QS_TXT, ANS_TXT, cors_id) VALUES ('" +\
          str(qs_id) + "','" + str(qs_txt) + "','" + str(ans_txt) + "','" + str(cors_txt) + "');"
    conn.execute(cmd)
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
    #print(search_result)
    conn.close()
    return search_result

#

def search_what_by_arg(what, db, table, wtf, arg):
    search_result = []
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    CMD = 'SELECT ' + str(what) + ' FROM ' + str(table) + ' WHERE ' + str(wtf) + " = '" + str(arg) + "' ;"
    print(CMD)
    cursor.execute(CMD)
    search_taple = cursor.fetchall()
    for element in search_taple:
        for el in element:
            search_result.append(el)
    conn.close()
    return search_result

#

def export_to_csv(db, table, csv_name):
    with sqlite3.connect(db) as connection:
        csvWriter = csv.writer(open(csv_name, "w"),  delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        c = connection.cursor()
        CMD = 'SELECT * FROM ' + str(table)
        c.execute(CMD)
        rows = c.fetchall()
        csvWriter.writerow(['ID Вопроса', 'Текст вопроса', 'Ответ респодента', 'ID респодента'])
        csvWriter.writerows(rows)

# Экспорт результатов в CSV файл.


def group(iterable, count):
    return zip(*[iter(iterable)] * count)

# Разбиение чего-то по count элементов


@app.route('/')
def main_page_task():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить рандомные вопросы в анкету': url_for('add_qs'),
              'Добавить новые вопросы вручную': url_for('add_qs_manual'),
              'Добавить готовые вопросы вручную': url_for('add_qs_chosen'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    return render_template('main.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5)


@app.route('/ch_wh_to_add')
def ch_wh_to_add():
    NAMES = download_txt_files()
    return render_template('ch_wh_to_add.html', NAMES = NAMES)


@app.route('/add_info')
def add_info():
    return render_template('add_info.html')


@app.route('/add_to_db')
def add_to_db():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить вопросы в анкету': url_for('add_qs'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    file_name = request.args['file_name']
    block_name_dirty = request.args['block_name']
    block_name = re.sub(' ', '_', block_name_dirty)
    question_text = open_file_read(file_name)
    question_text = question_text.split('\n')
    create_table_qs('List_of_qs')
    insert_task_qs(question_text, 'List_of_qs', block_name)
    urls_6 = {'Добавить еще один блок вопросов.': url_for('add_info'),
            }
    return render_template('add_to_db.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           urls_6=urls_6)


@app.route('/crt_form')
def crt_form():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить вопросы в анкету': url_for('add_qs'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    return render_template('crt_form.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5)


@app.route('/crt_form_fnl')
def crt_form_fnl():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить рандомные вопросы в анкету': url_for('add_qs'),
              'Добавить конкретные вопросы в анкету': url_for('add_qs_manual'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    form_name_dirty = request.args['form_name']
    form_name = re.sub(' ', '_', form_name_dirty)
    urls_6 = {'Перейти к добалению вопросов': url_for('add_qs'),
              }
    try:
        cmd = 'CREATE TABLE ' + str(form_name) + ' (QUESTION_ID   INTEGER   NOT NULL, QUESTION_TEXT   TEXT   NOT NULL)'
        conn.execute(cmd)
        conn.commit()
        conn.close()
        return render_template('crt_form_result.html', form_name=form_name, urls=urls, urls_2=urls_2, urls_3=urls_3,
                               urls_4=urls_4, urls_5=urls_5, urls_6=urls_6)
    except sqlite3.OperationalError:
        reply = 'При создании анкеты произошла ошибка, попробуйте другое имя.'
        print('error')
        return render_template('crt_form_error.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                               urls_5=urls_5, text=reply)


@app.route('/add_qs')
def add_qs():
    form_names = get_tables_names()
    block_names = get_block_name('List_of_qs_try')
    return render_template('add_qs.html', TABLES=form_names, BLOCKS=block_names)


@app.route('/add_qs_manual')
def add_qs_manual():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить рандомные вопросы в анкету': url_for('add_qs'),
              'Добавить конкретные вопросы в анкету': url_for('add_qs_manual'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    form_names = get_tables_names()
    return render_template('add_qs_manual.html', TABLES=form_names, urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5)


@app.route('/add_qs_manual_result')
def add_qs_manual_result():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить рандомные вопросы в анкету': url_for('add_qs'),
              'Добавить конкретные вопросы в анкету': url_for('add_qs_manual'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    form_name = request.args['form_name']
    block_name_dirty = request.args['block_name']
    block_name = re.sub(' ', '_', block_name_dirty)
    new_qs = request.args['new_qs']
    new_qs = new_qs.split('\r\n')
    if '        ' in new_qs:
        new_qs.remove('        ')
    for q in new_qs:
        insert_task_qs_2(q, 'List_of_qs_try', block_name)
        cmd = "SELECT QUESTION_ID,QUESTION_TEXT FROM List_of_qs_try WHERE QUESTION_TEXT = '" + str(q) + "'"
        cursor = conn.cursor()
        cursor.execute(cmd)
        group_of_items = cursor.fetchall()
        for element in group_of_items:
            cmd_add = 'INSERT INTO ' + str(form_name) + ' (QUESTION_ID, QUESTION_TEXT) VALUES (' + \
                      "'" + str(element[0]) + "','" + str(element[1]) + "'" + ');'
            conn.execute(cmd_add)
            conn.commit()
    qs_list = get_column('QS_And_Forms_DB.db', 'QUESTION_TEXT', form_name)
    return render_template('add_qs_result.html', urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5, qs_list=qs_list, form_name=form_name)


@app.route('/add_qs_chosen')
def add_qs_chosen():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить рандомные вопросы в анкету': url_for('add_qs'),
              'Добавить конкретные вопросы в анкету': url_for('add_qs_manual'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    form_names = get_tables_names()
    qs_list = get_column('QS_And_Forms_DB.db', 'QUESTION_TEXT', 'List_of_qs_try')
    return render_template('add_qs_chosen.html', TABLES=form_names, QS=qs_list, urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5)


@app.route('/add_qs_chosen_result')
def add_qs_chosen_result():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить рандомные вопросы в анкету': url_for('add_qs'),
              'Добавить конкретные вопросы в анкету': url_for('add_qs_manual'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    form_name = request.args['form_name']
    qs = request.args['qs']
    cmd = "SELECT QUESTION_ID,QUESTION_TEXT FROM List_of_qs_try WHERE QUESTION_TEXT = '" + str(qs) + "'"
    cursor = conn.cursor()
    cursor.execute(cmd)
    group_of_items = cursor.fetchall()
    print(len(group_of_items))
    if len(group_of_items) > 1:
        print(group_of_items[0])
        print(group_of_items[0][0])
        print(group_of_items[0][1])
        cmd_add = 'INSERT INTO ' + str(form_name) + ' (QUESTION_ID, QUESTION_TEXT) VALUES (' + \
                  "'" + str(group_of_items[0][0]) + "','" + str(group_of_items[0][1]) + "'" + ');'
        conn.execute(cmd_add)
        conn.commit()
    else:
        for element in group_of_items:
            cmd_add = 'INSERT INTO ' + str(form_name) + ' (QUESTION_ID, QUESTION_TEXT) VALUES (' + \
                      "'" + str(element[0]) + "','" + str(element[1]) + "'" + ');'
            conn.execute(cmd_add)
            conn.commit()
    qs_list = get_column('QS_And_Forms_DB.db', 'QUESTION_TEXT', form_name)
    return render_template('add_qs_result.html', urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5, qs_list=qs_list, form_name=form_name)


@app.route('/add_qs_result')
def add_qs_result():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить рандомные вопросы в анкету': url_for('add_qs'),
              'Добавить конкретные вопросы в анкету': url_for('add_qs_manual'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    amount = int(request.args['amount'])
    form_name = request.args['form_name']
    block_name = request.args['block_name']
    max_amount = get_block_qs_amount('List_of_qs_try', block_name)
    if amount <= max_amount:
        cmd = "SELECT QUESTION_ID,QUESTION_TEXT FROM List_of_qs_try WHERE QUESTION_BLOCK = '" + str(block_name) + "'"
        cursor = conn.cursor()
        cursor.execute(cmd)
        group_of_items = cursor.fetchall()
        list_of_random_items = random.sample(group_of_items, amount)
        for element in list_of_random_items:
            cmd_add = 'INSERT INTO ' + str(form_name) + ' (QUESTION_ID, QUESTION_TEXT) VALUES (' +\
                          "'" + str(element[0]) + "','" + str(element[1]) + "'" + ');'
            conn.execute(cmd_add)
            conn.commit()
        qs_list = get_column('QS_And_Forms_DB.db', 'QUESTION_TEXT', form_name)
        return render_template('add_qs_result.html', urls=urls, urls_2=urls_2, urls_3=urls_3,
                               urls_4=urls_4, urls_5=urls_5, qs_list=qs_list, form_name=form_name)
    else:
        return render_template('add_qs_error.html')


@app.route('/select_form')
def select_form():
    tables = get_tables_names()
    list_of_names = list(group(get_column('cors_info.db', 'name, id', 'cors_info'), 2))
    print(list_of_names)
    return render_template('cmp_form.html', TABLES=tables, names=list_of_names)


@app.route('/open_form')
def open_form():
    form_name = request.args['selected_form']
    cors_id = request.args['cors_id']
    session['cid'] = cors_id
    session['fn'] = form_name
    list_of_qs = get_column('QS_And_Forms_DB.db', 'QUESTION_TEXT', form_name)
    print(list_of_qs)
    print(session['fn'])
    return render_template('open_form.html', List_Q=list_of_qs)


@app.route('/check_ans')
def check_ans():
    d = {}
    form_info = list(group(get_column('QS_And_Forms_DB.db', '*', session['fn']), 2))
    for element in form_info:
        answers = []
        ans = request.args[element[1]]
        answers.append(ans)
        answers.append(element[1])
        d[str(element[0])] = answers
    session['memory'] = d
    print(session)
    return render_template('check_ans.html', memory=d)


@app.route('/add_ans')
def add_ans():
    cors_id = session['cid']
    info = session['memory']
    for el in info:
        add_ans_fnc(str(el), str(info[el][1]), str(info[el][0]), str(cors_id))
    return render_template('add_ans.html')


@app.route('/search_id')
def search_id():
    search_args = set(search_task('ANS_Db.db', 'ALL_ANS', 'QS_ID'))
    print(search_args)
    return render_template('search_id.html', info=search_args)


@app.route('/search_id_result')
def search_id_result():
    q_id = request.args['id']
    result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'QS_ID', q_id)
    print(result)
    result2 = list(group(result, 4))
    print(result2)
    return render_template('search_id_result.html', q_id=q_id, result=result2)


@app.route('/search_name')
def search_name():
    search_args = search_task('cors_info.db', 'cors_info', 'name')
    print(search_args)
    return render_template('search_name.html', info=search_args)


@app.route('/search_name_result')
def search_name_result():
    name = request.args['name']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'name', name)
    for el in my_id:
        result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        print(result)
    result2 = list(group(result, 4))
    print(result2)
    return render_template('search_name_result.html', name=name, result=result2)


@app.route('/search_year')
def search_year():
    search_args = search_task('cors_info.db', 'cors_info', 'year')
    print(search_args)
    return render_template('search_year.html', info=search_args)


@app.route('/search_year_result')
def search_year_result():
    year = request.args['year']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'year', year)
    for el in my_id:
        result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        print(result)
    result2 = list(group(result, 4))
    print(result2)
    return render_template('search_year_result.html', year=year, result=result2)


@app.route('/search_town')
def search_town():
    search_args = search_task('cors_info.db', 'cors_info', 'town')
    print(search_args)
    return render_template('search_town.html', info=search_args)


@app.route('/search_town_result')
def search_town_result():
    town = request.args['town']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'town', town)
    for el in my_id:
        result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        print(result)
    result2 = list(group(result, 4))
    print(result2)
    return render_template('search_town_result.html', town=town, result=result2)

@app.route('/search_gender')
def search_gender():
    search_args = search_task('cors_info.db', 'cors_info', 'gender')
    print(search_args)
    search_args = set(search_args)
    return render_template('search_gender.html', info=search_args)


@app.route('/search_gender_result')
def search_gender_result():
    gender = request.args['gender']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'gender', gender)
    for el in my_id:
        result = search_what_by_arg('QS_ID, QS_TXT, ANS_TXT, cors_id', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        print(result)
    result2 = list(group(result, 4))
    print(result2)
    return render_template('search_gender_result.html', gender=gender, result=result2)


@app.route('/add_cors')
def add_cors():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить вопросы в анкету': url_for('add_qs'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    return render_template('add_cors.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5)


@app.route('/add_cors_fin')
def add_cors_fin():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить вопросы в анкету': url_for('add_qs'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    name = request.args['name']
    year = request.args['year']
    gender = request.args['gender']
    town = request.args['town']
    additional_info = request.args['additional_info']
    raw1 = "'" + str(name) + "','" + str(year) + "','" + str(town) + "','" + str(gender) + "','" + str(additional_info) + "'"
    raw2 = 'name, year, town, gender, additional_info'
    add_info_to_db('cors_info.db', 'cors_info', raw2, str(raw1))
    cors_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'name', str(name))
    return render_template('add_cors_result.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           name=name, cors_id=cors_id)


@app.route('/convert_ans')
def convert_ans():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить вопросы в анкету': url_for('add_qs'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    try:
        export_to_csv('ANS_DB.db', 'ALL_ANS', 'output_ans.csv')
        return render_template('convert_to_csv.html', file_name='output_ans.csv', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5)
    except BaseException:
        return render_template('convert_to_csv_error.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5)


@app.route('/convert_qs')
def convert_qs():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить вопросы в анкету': url_for('add_qs'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    try:
        export_to_csv('ANS_DB.db', 'ALL_ANS', 'output_qs.csv')
        return render_template('convert_to_csv.html', file_name='output_qs.csv', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5)
    except BaseException:
        return render_template('convert_to_csv_error.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5)


@app.route('/convert_cons')
def convert_cons():
    urls = {'Добавить вопросы в DB': url_for('add_info'),
            }
    urls_2 = {'Создать анкету': url_for('crt_form'),
              'Добавить корисподента': url_for('add_cors'),
              'Добавить вопросы в анкету': url_for('add_qs'),
              }
    urls_3 = {'Пройти готовую анкету': url_for('select_form'),
              }
    urls_4 = {'Поиск по id вопроса': url_for('search_id'),
              'Поиск по имени рс-нт': url_for('search_name'),
              'Поиск по возрасту рс-нт': url_for('search_year'),
              'Поиск по городу рс-нта': url_for('search_town'),
              'Поиск по полу': url_for('search_gender'),
              }
    urls_5 = {'Экспорт ответов': url_for('convert_ans'),
              'Экспорт вопросов': url_for('convert_qs'),
              'Экспорт кор. инф.': url_for('convert_cons'),
              }
    try:
        export_to_csv('ANS_DB.db', 'ALL_ANS', 'output_ans.csv')
        return render_template('convert_to_csv.html', file_name='output_cons.csv', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5)
    except BaseException:
        return render_template('convert_to_csv_error.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5)

if __name__ == '__main__':
    app.run(debug=True)
