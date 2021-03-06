from flask import Flask, session
from flask import url_for, render_template, request
import sqlite3
import random
import csv
import re
import os


app = Flask(__name__)
key = os.urandom(24)
app.secret_key = key

urls_main = {'Главная': 'http://127.0.0.1:5000/',
             }
urls = {'Загрузить вопросы из файла': 'http://127.0.0.1:5000/add_info',
        'Загрузить вопросы вручную': 'http://127.0.0.1:5000/add_info_manual'
        }
urls_2 = {'Создать анкету': 'http://127.0.0.1:5000/crt_form',
          'Добавить респондента': 'http://127.0.0.1:5000/add_cors',
          'Добавить рандомные вопросы в анкету': 'http://127.0.0.1:5000/add_qs',
          'Добавить новые вопросы в анкету': 'http://127.0.0.1:5000/add_qs_manual',
          'Добавить конкретные вопросы в анкету': 'http://127.0.0.1:5000/add_qs_chosen',
          }
urls_3 = {'Пройти готовую анкету': 'http://127.0.0.1:5000/select_form',
          }
urls_4 = {'Поиск по id вопроса': 'http://127.0.0.1:5000/search_id',
          'Поиск по имени рс-нт': 'http://127.0.0.1:5000/search_name',
          'Поиск по возрасту рс-нт': 'http://127.0.0.1:5000/search_year',
          'Поиск по городу рс-нта': 'http://127.0.0.1:5000/search_town',
          'Поиск по полу': 'http://127.0.0.1:5000/search_gender',
          'Поиск вхождения в ответах': 'http://127.0.0.1:5000/search_reply',
          }
urls_5 = {'Экспорт ответов': 'http://127.0.0.1:5000/convert_ans',
          'Экспорт вопросов': 'http://127.0.0.1:5000/convert_qs',
          'Экспорт респ. инф.': 'http://127.0.0.1:5000/convert_cons',
          }


def add_info_to_db(db, table, where, what):
    conn = sqlite3.connect(str(db))
    cmd = 'INSERT INTO ' + table + ' (' + where + ') VALUES (' + what + ');'
    conn.execute(cmd)
    conn.commit()
    conn.close()


def open_file_read(NAME):
    opening_file = open(NAME, 'r', encoding='UTF-8')
    text = opening_file.read()
    opening_file.close()
    return text


def open_file_line(NAME):
    opening_file = open(NAME, 'r', encoding='UTF-8')
    text = opening_file.readlines()
    opening_file.close()
    return text


def download_txt_files():
    txt_files = []
    all_files = os.listdir()
    for element in all_files:
        if element.endswith('.txt'):
            txt_files.append(element)
    return txt_files


def create_table_qs(table_name):
    try:
        conn = sqlite3.connect('QS_And_Forms_DB.db')
        cmd = 'CREATE TABLE ' + table_name +\
              ' (QUESTION_ID   INTEGER NOT NULL PRIMARY' \
              ' KEY AUTOINCREMENT, QUESTION_TEXT   TEXT   NOT NULL,' \
              ' QUESTION_BLOCK   TEXT   NOT NULL)'
        conn.execute(cmd)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print('        table exist         ')


def create_table_forms(table_name):     # Создание таблицы для форм
    try:
        conn = sqlite3.connect('QS_And_Forms_DB.db')
        cmd = 'CREATE TABLE ' + table_name + ' (QUESTION_ID   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                                             ' QUESTION_TEXT   TEXT   NOT NULL,)'
        conn.execute(cmd)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print('        table exist         ')


def insert_task_qs(QT, TABLE_NAME, BLOCK_NAME):
    for element in QT:
        conn = sqlite3.connect('QS_And_Forms_DB.db')
        COMMAND = 'INSERT INTO ' + TABLE_NAME + ' (QUESTION_TEXT, QUESTION_BLOCK) VALUES (' + "'" + element + "','" +\
                  BLOCK_NAME + "'" +');'
        conn.execute(COMMAND)
        conn.commit()
        conn.close()


def insert_task_qs_2(QT, TABLE_NAME, BLOCK_NAME):
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    сmd = 'INSERT INTO ' + TABLE_NAME + ' (QUESTION_TEXT, QUESTION_BLOCK) VALUES (' + "'" + QT + "','" + BLOCK_NAME +\
          "'" +');'
    conn.execute(сmd)
    conn.commit()
    conn.close()


def get_tables_names():
    final_list = []
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    cursor = conn.cursor()
    cmd = 'SELECT NAME FROM sqlite_master WHERE type=' + "'" + 'table' + "'" + 'ORDER BY name;'
    cursor.execute(cmd)
    list_of_names = cursor.fetchall()
    for element in list_of_names:
        for el in element:
            final_list.append(el)
    conn.close()
    return final_list


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
    final_list = []
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    cursor = conn.cursor()
    cmd = 'SELECT QUESTION_BLOCK FROM ' + TABLE_NAME
    cursor.execute(cmd)
    list_of_names = cursor.fetchall()
    for element in list_of_names:
        for el in element:
            final_list.append(el)
    conn.close()
    return set(final_list)


def get_block_qs_amount(TABLE_NAME, arg):
    qs_list = []
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    cursor = conn.cursor()
    cmd = 'SELECT QUESTION_TEXT FROM ' + str(TABLE_NAME) + " WHERE QUESTION_BLOCK = '" + str(arg) + "' ;"
    cursor.execute(cmd)
    list_of_names = cursor.fetchall()
    for element in list_of_names:
        for el in element:
            qs_list.append(el)
    conn.close()
    return len(qs_list)


def add_ans_fnc(qs_id, qs_txt, ans_txt, cors_txt, comments):
    conn = sqlite3.connect('ANS_DB.db')
    try:
        cmd = 'CREATE TABLE ALL_ANS (QS_ID   INTEGER NOT NULL , QS_TXT   TEXT   NOT NULL, ANS_TXT TEXT NOT NULL,' \
              ' cors_id   INTEGER NOT NULL, comments   TEXT   NOT NULL)'
        conn.execute(cmd)
    except sqlite3.OperationalError:
        print('        table exist         ')
    cmd = "INSERT INTO ALL_ANS (QS_ID, QS_TXT, ANS_TXT, cors_id, comments) VALUES ('" +\
          str(qs_id) + "','" + str(qs_txt) + "','" + str(ans_txt) + "','" + str(cors_txt) +\
          "','" + str(comments) + "');"
    conn.execute(cmd)
    conn.commit()
    conn.close()


def search_task(db, table, uprise):
    search_result = []
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cmd = 'SELECT ' + str(uprise) + ' FROM ' + str(table)
    cursor.execute(cmd)
    search_taple = cursor.fetchall()
    for element in search_taple:
        for el in element:
            search_result.append(el)
    conn.close()
    return search_result


def search_what_by_arg(what, db, table, wtf, arg):
    search_result = []
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cmd = 'SELECT ' + str(what) + ' FROM ' + str(table) + ' WHERE ' + str(wtf) + " = '" + str(arg) + "' ;"
    cursor.execute(cmd)
    search_table = cursor.fetchall()
    for element in search_table:
        for el in element:
            search_result.append(el)
    conn.close()
    return search_result


def export_to_csv(db, table, csv_name, argument):
    with sqlite3.connect(db) as connection:
        arg = argument
        csvWriter = csv.writer(open(csv_name, "w"),  delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        c = connection.cursor()
        cmd = 'SELECT * FROM ' + str(table)
        c.execute(cmd)
        rows = c.fetchall()
        if arg == 'resp_info':
            row = ['ID респондента', 'ФИО респондента', 'Город рождения респондента', 'Пол респондента',
                   'Дополнительная информаци']
        elif arg == 'reply':
            row = ['ID Вопроса', 'Текст вопроса', 'Ответ респодента', 'ID респодента', 'Комментарий пользователя']
        elif arg == 'qs':
            row = ['ID Вопроса', 'Текст вопроса', 'Блок вопросов']
        csvWriter.writerow(row)
        csvWriter.writerows(rows)


def group(iterable, count):
    return zip(*[iter(iterable)] * count)


@app.route('/')
def main_page_task():
    return render_template('main.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           urls_main=urls_main)


@app.route('/add_info')
def add_info():
    return render_template('add_info.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           urls_main=urls_main)


@app.route('/add_info_manual')
def add_info_manual():
    blocks = set(get_column('QS_And_Forms_DB.db', 'QUESTION_BLOCK', 'List_of_qs'))
    return render_template('add_info_manual.html', blocks=blocks, urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/add_info_manual_result')
def add_info_manual_result():
    block_name = request.args['block_name']
    new_block_name = request.args['new_block_name']
    new_block_name = re.sub(' ', '_', new_block_name)
    new_qs = request.args['new_qs']
    new_qs = new_qs.split('\r\n')
    if '        ' in new_qs:
        new_qs.remove('        ')
    if new_block_name != '':
        for q in new_qs:
            insert_task_qs_2(q, 'List_of_qs', new_block_name)
    else:
        for q in new_qs:
            insert_task_qs_2(q, 'List_of_qs', block_name)
    urls_6 = {'Добавить еще один блок вопросов.': url_for('add_info'),
            }
    return render_template('add_to_db.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           urls_main=urls_main, urls_6=urls_6)


@app.route('/add_to_db')
def add_to_db():
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
                           urls_main=urls_main, urls_6=urls_6)


@app.route('/crt_form')
def crt_form():
    return render_template('crt_form.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           urls_main=urls_main)


@app.route('/crt_form_fnl')
def crt_form_fnl():
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
                               urls_4=urls_4, urls_5=urls_5, urls_main=urls_main, urls_6=urls_6)
    except sqlite3.OperationalError:
        reply = 'При создании анкеты произошла ошибка, попробуйте другое имя.'
        print('error')
        return render_template('crt_form_error.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                               urls_5=urls_5, urls_main=urls_main, text=reply)


@app.route('/add_qs')
def add_qs():
    form_names = get_tables_names()
    form_names.remove('List_of_qs')
    form_names.remove('sqlite_sequence')
    block_names = get_block_name('List_of_qs')
    return render_template('add_qs.html', TABLES=form_names, BLOCKS=block_names, urls=urls, urls_2=urls_2,
                           urls_3=urls_3, urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/add_qs_manual')
def add_qs_manual():
    form_names = get_tables_names()
    form_names.remove('List_of_qs')
    form_names.remove('sqlite_sequence')
    return render_template('add_qs_manual.html', TABLES=form_names, urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/add_qs_manual_result')
def add_qs_manual_result():
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    form_name = request.args['form_name']
    block_name_dirty = request.args['block_name']
    block_name = re.sub(' ', '_', block_name_dirty)
    new_qs = request.args['new_qs']
    new_qs = new_qs.split('\r\n')
    if '        ' in new_qs:
        new_qs.remove('        ')
    for q in new_qs:
        insert_task_qs_2(q, 'List_of_qs', block_name)
        cmd = "SELECT QUESTION_ID,QUESTION_TEXT FROM List_of_qs WHERE QUESTION_TEXT = '" + str(q) + "'"
        cursor = conn.cursor()
        cursor.execute(cmd)
        group_of_items = cursor.fetchall()
        for element in group_of_items:
            cmd_add = 'INSERT INTO ' + str(form_name) + ' (QUESTION_ID, QUESTION_TEXT) VALUES (' + \
                      "'" + str(element[0]) + "','" + str(element[1]) + "'" + ');'
            conn.execute(cmd_add)
            conn.commit()
    qs_list = get_column('QS_And_Forms_DB.db', 'QUESTION_TEXT', form_name)
    return render_template('add_qs_result.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           urls_main=urls_main, qs_list=qs_list, form_name=form_name)


@app.route('/add_qs_chosen')
def add_qs_chosen():
    form_names = get_tables_names()
    form_names.remove('List_of_qs')
    form_names.remove('sqlite_sequence')
    qs_list = get_column('QS_And_Forms_DB.db', 'QUESTION_TEXT', 'List_of_qs')
    return render_template('add_qs_chosen.html', TABLES=form_names, urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5, urls_main=urls_main, QS=qs_list)


@app.route('/add_qs_chosen_result')
def add_qs_chosen_result():
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    form_name = request.args['form_name']
    qs = request.args['qs']
    cmd = "SELECT QUESTION_ID,QUESTION_TEXT FROM List_of_qs WHERE QUESTION_TEXT = '" + str(qs) + "'"
    cursor = conn.cursor()
    cursor.execute(cmd)
    group_of_items = cursor.fetchall()
    if len(group_of_items) > 1:
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
    return render_template('add_qs_result.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           urls_main=urls_main, qs_list=qs_list, form_name=form_name)


@app.route('/add_qs_result')
def add_qs_result():
    conn = sqlite3.connect('QS_And_Forms_DB.db')
    amount = int(request.args['amount'])
    form_name = request.args['form_name']
    block_name = request.args['block_name']
    max_amount = get_block_qs_amount('List_of_qs', block_name)
    if amount <= max_amount:
        cmd = "SELECT QUESTION_ID,QUESTION_TEXT FROM List_of_qs WHERE QUESTION_BLOCK = '" + str(block_name) + "'"
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
        return render_template('add_qs_result.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                               urls_5=urls_5, urls_main=urls_main, qs_list=qs_list, form_name=form_name)
    else:
        return render_template('add_qs_error.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                               urls_5=urls_5, urls_main=urls_main)


@app.route('/select_form')
def select_form():
    tables = get_tables_names()
    tables.remove('List_of_qs')
    tables.remove('sqlite_sequence')
    list_of_names = list(group(get_column('cors_info.db', 'name, id', 'cors_info'), 2))
    return render_template('cmp_form.html', TABLES=tables, names=list_of_names, urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/open_form')
def open_form():
    form_name = request.args['selected_form']
    cors_id = request.args['cors_id']
    session['cid'] = cors_id
    session['fn'] = form_name
    list_of_qs = get_column('QS_And_Forms_DB.db', 'QUESTION_TEXT', form_name)
    return render_template('open_form.html', List_Q=list_of_qs, urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                           urls_5=urls_5, urls_main=urls_main)


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
    return render_template('check_ans.html', memory=d, urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                           urls_5=urls_5, urls_main=urls_main)


@app.route('/add_ans')
def add_ans():
    i = 0
    cors_id = session['cid']
    info = session['memory']
    for el in info:
        comment_id = 'comments' + str(el)
        comments = request.args[str(comment_id)]
        add_ans_fnc(str(el), str(info[el][1]), str(info[el][0]), str(cors_id), str(comments))
        i += 1
    return render_template('add_ans.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           urls_main=urls_main)


@app.route('/search_id')
def search_id():
    search_args = set(search_task('ANS_Db.db', 'ALL_ANS', 'QS_ID'))
    return render_template('search_id.html', info=search_args, urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                           urls_5=urls_5, urls_main=urls_main)


@app.route('/search_id_result')
def search_id_result():
    q_id = request.args['id']
    result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'QS_ID', q_id)
    result2 = list(group(result, 5))
    return render_template('search_id_result.html', q_id=q_id, result=result2, urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/search_name')
def search_name():
    search_args = search_task('cors_info.db', 'cors_info', 'name')
    search_args = set(search_args)
    return render_template('search_name.html', info=search_args, urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                           urls_5=urls_5, urls_main=urls_main)


@app.route('/search_name_result')
def search_name_result():
    result_out = []
    name = request.args['name']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'name', name)
    for el in my_id:
        result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        if result != []:
            for el in result:
                result_out.append(el)
    result2 = list(group(result_out, 5))
    return render_template('search_name_result.html', name=name, result=result2, urls=urls, urls_2=urls_2,
                           urls_3=urls_3, urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/search_year')
def search_year():
    search_args = search_task('cors_info.db', 'cors_info', 'year')
    search_args = set(search_args)
    return render_template('search_year.html', info=search_args, urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                           urls_5=urls_5, urls_main=urls_main)


@app.route('/search_year_result')
def search_year_result():
    result_out = []
    year = request.args['year']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'year', year)
    for el in my_id:
        result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        if result != []:
            for el in result:
                result_out.append(el)
    result2 = list(group(result_out, 5))
    return render_template('search_year_result.html', year=year, result=result2, urls=urls, urls_2=urls_2,
                           urls_3=urls_3, urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/search_town')
def search_town():
    search_args = search_task('cors_info.db', 'cors_info', 'town')
    search_args = set(search_args)
    return render_template('search_town.html', info=search_args, urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                           urls_5=urls_5, urls_main=urls_main)


@app.route('/search_town_result')
def search_town_result():
    result_out = []
    town = request.args['town']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'town', town)
    for el in my_id:
        result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        if result != []:
            for el in result:
                result_out.append(el)
    result2 = list(group(result_out, 5))
    return render_template('search_town_result.html', town=town, result=result2, urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           urls_main=urls_main)


@app.route('/search_gender')
def search_gender():
    search_args = search_task('cors_info.db', 'cors_info', 'gender')
    search_args = set(search_args)
    return render_template('search_gender.html', info=search_args, urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/search_gender_result')
def search_gender_result():
    result_out = []
    gender = request.args['gender']
    my_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'gender', gender)
    for el in my_id:
        result = search_what_by_arg('*', 'ANS_DB.db', 'ALL_ANS', 'cors_id', el)
        if result != []:
            for el in result:
                result_out.append(el)
    result2 = list(group(result_out, 5))
    if gender == 'Мужской':
        gender = 'Мужского'
    else:
        gender = 'Женского'
    return render_template('search_gender_result.html', gender=gender, result=result2, urls=urls, urls_2=urls_2,
                           urls_3=urls_3, urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/search_reply')
def search_reply():
    return render_template('search_reply.html', urls=urls, urls_2=urls_2, urls_3=urls_3,
                           urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/search_reply_result')
def search_reply_result():
    result_list = []
    reply_list = search_task('ANS_DB.db', 'ALL_ANS', 'ANS_TXT')
    qs_list = search_task('ANS_DB.db', 'ALL_ANS', 'QS_TXT')
    key_word = request.args['key_word']
    print(key_word)
    print(reply_list)
    i = 0
    for reply in reply_list:
        block = []
        print(reply)
        reply = reply.lower()
        words = reply.split()
        for word in words:
            if key_word == word:
                block.append(qs_list[i])
                block.append(reply)
                print(block)
                result_list.append(block)
        i += 1
    print(result_list)
    return render_template('search_reply_result.html', key_word=key_word, result=result_list, urls=urls, urls_2=urls_2,
                           urls_3=urls_3, urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)


@app.route('/add_cors')
def add_cors():
    return render_template('add_resp.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4, urls_5=urls_5,
                           urls_main=urls_main)


@app.route('/add_cors_fin')
def add_cors_fin():
    name = request.args['name']
    year = request.args['year']
    gender = request.args['gender']
    town = request.args['town']
    additional_info = request.args['additional_info']
    raw1 = "'" + str(name) + "','" + str(year) + "','" + str(town) + "','" + str(gender) + "','" +\
           str(additional_info) + "'"
    raw2 = 'name, year, town, gender, additional_info'
    add_info_to_db('cors_info.db', 'cors_info', raw2, str(raw1))
    cors_id = search_what_by_arg('id', 'cors_info.db', 'cors_info', 'name', str(name))
    return render_template('add_resp_result.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                           urls_5=urls_5, urls_main=urls_main, name=name, cors_id=cors_id)


@app.route('/convert_ans')
def convert_ans():
    try:
        export_to_csv('ANS_DB.db', 'ALL_ANS', 'output_ans.csv', 'reply')
        return render_template('convert_to_csv.html', file_name='output_ans.csv', urls=urls, urls_2=urls_2,
                               urls_3=urls_3, urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)
    except BaseException:
        return render_template('convert_to_csv_error.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                               urls_5=urls_5, urls_main=urls_main)


@app.route('/convert_qs')
def convert_qs():
    try:
        export_to_csv('QS_And_Forms_DB.db', 'List_of_qs', 'output_qs.csv', 'qs')
        return render_template('convert_to_csv.html', file_name='output_qs.csv', urls=urls, urls_2=urls_2,
                               urls_3=urls_3, urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)
    except BaseException:
        return render_template('convert_to_csv_error.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                               urls_5=urls_5, urls_main=urls_main)


@app.route('/convert_cons')
def convert_cons():
    try:
        export_to_csv('cors_info.db', 'cors_info', 'output_resp_info.csv', 'resp_info')
        return render_template('convert_to_csv.html', file_name='output_cons.csv', urls=urls, urls_2=urls_2,
                               urls_3=urls_3, urls_4=urls_4, urls_5=urls_5, urls_main=urls_main)
    except BaseException:
        return render_template('convert_to_csv_error.html', urls=urls, urls_2=urls_2, urls_3=urls_3, urls_4=urls_4,
                               urls_5=urls_5, urls_main=urls_main)

if __name__ == '__main__':
    app.run(debug=True)
