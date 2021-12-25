import sqlite3

from settings import *
import ast
import requests
import json
from random import randint
import pyqiwi
                                    #-#-#-#-#-#-#-#-#-#BEGINNING#-#-#-#-#-#-#-#-#-#
def pay_seller(amount):
    wallet = pyqiwi.Wallet(token=api_qiwi,number=num_qiwi)
    wallet.qiwi_transfer(num_qiwi_seller,int(amount))

def create_order(id):
    id1 = id
    conn = sqlite3.connect('db.db')
    q = conn.cursor()
    try:
        q.execute(f'DELETE FROM check_payment WHERE id IS "{id1}"')
    except:
        pass
    q.execute('INSERT INTO check_payment VALUES (?,?,?)', (id1, total_cheque(id1)[0],randint(1,999999999)))
    conn.commit()


def check_payment(id):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    try:
        session = requests.Session()
        session.headers['authorization'] = 'Bearer ' + api_qiwi
        parameters = {'rows': '5'}
        h = session.get('https://edge.qiwi.com/payment-history/v1/persons/{}/payments'.format(num_qiwi),
                        params=parameters)
        req = json.loads(h.text)
        result = cursor.execute(f'SELECT * FROM check_payment WHERE id = {id}').fetchone()
        comment = result[2]
        sum = result[1]
        for i in range(len(req['data'])):
            if str(comment) in str(req['data'][i]['comment']) and str('643') in str(req['data'][i]["sum"]["currency"]) and str(sum) in str(req['data'][i]["sum"]["amount"]):
                return req["data"][i]["sum"]["amount"]
    except Exception as e:
        print(e)
    conn.close()


def first_join(id):
    conn = sqlite3.connect('db.db')
    q = conn.cursor()
    q.execute("INSERT INTO users VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(id, [], [], [], [], [], [], [], [], 0))
    conn.commit()
    conn.close()

def info_user(id):
    conn = sqlite3.connect('db.db')
    q = conn.cursor()
    q.execute("SELECT cocacola FROM users WHERE id IS "+str(id))
    q = [*q]
    if q == []:
        return 'new'
    else:
        return 'ok'


                                    #-#-#-#-#-#-#-#-#-#LETSGOOOOOOO#-#-#-#-#-#-#-#-#-#


def separator(data,id):
    first_part = data.split(':')[0]
    second_part = data.split(':')[1]
    conn = sqlite3.connect('db.db')
    q = conn.cursor()
    q.execute(f"SELECT {second_part} FROM users WHERE id IS "+str(id))
    q_new = [*q][0][0]
    x = ast.literal_eval(q_new)
    x.append(first_part)
    if second_part == 'fanta':
        q.execute(f'UPDATE users SET fanta="{x}" WHERE id IS "{id}"')
    elif second_part == 'cocacola':
        q.execute(f'UPDATE users SET cocacola="{x}" WHERE id IS "{id}"')
    elif second_part == 'pepsicola':
        q.execute(f'UPDATE users SET pepsicola="{x}" WHERE id IS "{id}"')
    elif second_part == 'sprite':
        q.execute(f'UPDATE users SET sprite="{x}" WHERE id IS "{id}"')
    elif second_part == 'pulpy':
        q.execute(f'UPDATE users SET pulpy="{x}" WHERE id IS "{id}"')
    elif second_part == 'crush':
        q.execute(f'UPDATE users SET crush="{x}" WHERE id IS "{id}"')
    elif second_part == 'natakhtari':
        q.execute(f'UPDATE users SET natakhtari="{x}" WHERE id IS "{id}"')
    elif second_part == 'fanta':
        q.execute(f'UPDATE users SET fanta="{x}" WHERE id IS "{id}"')
    elif second_part == 'milkis':
        q.execute(f'UPDATE users SET milkis="{x}" WHERE id IS "{id}"')
    conn.commit()
    conn.close()

def reset_cart(id):
    conn = sqlite3.connect('db.db')
    q = conn.cursor()
    q.execute(f'UPDATE users SET fanta="[]" WHERE id IS "{id}"')
    q.execute(f'UPDATE users SET cocacola="[]" WHERE id IS "{id}"')
    q.execute(f'UPDATE users SET pepsicola="[]" WHERE id IS "{id}"')
    q.execute(f'UPDATE users SET sprite="[]" WHERE id IS "{id}"')
    q.execute(f'UPDATE users SET pulpy="[]" WHERE id IS "{id}"')
    q.execute(f'UPDATE users SET crush="[]" WHERE id IS "{id}"')
    q.execute(f'UPDATE users SET natakhtari="[]" WHERE id IS "{id}"')
    q.execute(f'UPDATE users SET milkis="[]" WHERE id IS "{id}"')
    q.execute(f'UPDATE users SET total ="0" WHERE id IS "{id}"')
    conn.commit()
    conn.close()

def total_cheque(id):
    s = 0
    conn = sqlite3.connect('db.db')
    q = conn.cursor()
    sum_cocacola = 0
    try:
        q.execute("SELECT cocacola FROM users WHERE id IS " + str(id))
        q_new = [*q][0][0]
        x = ast.literal_eval(q_new)
        a = len(x)
        s = s + a
        sum_cocacola = a * cocacola_cost
    except:
        pass
    sum_pepsicola = 0
    try:
        q.execute("SELECT pepsicola FROM users WHERE id IS " + str(id))
        q_new = [*q][0][0]
        x = ast.literal_eval(q_new)
        a = len(x)
        sum_pepsicola = a * pepsicola_cost
        s = s + a
    except:
        pass
    sum_sprite = 0
    try:
        q.execute("SELECT sprite FROM users WHERE id IS " + str(id))
        q_new = [*q][0][0]
        x = ast.literal_eval(q_new)
        a = len(x)
        sum_sprite = a * sprite_cost
        s = s + a
    except:
        pass
    sum_fanta = 0
    try:
        q.execute("SELECT fanta FROM users WHERE id IS " + str(id))
        q_new = [*q][0][0]
        x = ast.literal_eval(q_new)
        a = len(x)
        sum_fanta = a * fanta_cost
        s = s + a
    except:
        pass
    sum_crush = 0
    try:
        q.execute("SELECT crush FROM users WHERE id IS " + str(id))
        q_new = [*q][0][0]
        x = ast.literal_eval(q_new)
        a = len(x)
        sum_crush = a * crush_cost
        s = s + a
    except:
        pass
    sum_natakhtari = 0
    try:
        q.execute("SELECT natakhtari FROM users WHERE id IS " + str(id))
        q_new = [*q][0][0]
        x = ast.literal_eval(q_new)
        a = len(x)
        sum_natakhtari = a * natakhtari_cost
        s = s + a
    except:
        pass
    sum_milkis = 0
    try:
        q.execute("SELECT milkis FROM users WHERE id IS " + str(id))
        q_new = [*q][0][0]
        x = ast.literal_eval(q_new)
        a = len(x)
        conn.close()
        sum_milkis = a * milkis_cost
        s = s + a
    except:
        pass
    total = sum_cocacola + sum_pepsicola + sum_sprite + sum_fanta + sum_crush + sum_natakhtari + sum_milkis
    return [total,s]

def all_in_list(id):
    conn = sqlite3.connect('db.db')
    q = conn.cursor()
    q.execute('SELECT * FROM users WHERE id IS '+str(id))
    q = [*q]
    q = q[0][1:9]
    list = []
    for elem in q:
        list.append(elem)
    return list

def delete_code(id):
    conn = sqlite3.connect('db.db')
    q = conn.cursor()
    q.execute('DELETE FROM check_payment WHERE id IS '+str(id))
    conn.commit()
    conn.close()

def include(id):
    list_with_all = all_in_list(id)
    all_cocacola = list_with_all[0]
    all_cocacola = ast.literal_eval(all_cocacola)
    print(all_cocacola)
    all_pepsicola = list_with_all[1]
    all_pepsicola = ast.literal_eval(all_pepsicola)
    print(all_pepsicola)
    all_sprite = list_with_all[2]
    all_sprite = ast.literal_eval(all_sprite)
    print(all_sprite)
    all_pulpy = list_with_all[3]
    all_pulpy = ast.literal_eval(all_pulpy)
    print(all_pulpy)
    all_crush = list_with_all[4]
    all_crush = ast.literal_eval(all_crush)
    print(all_crush)
    all_natakhtari = list_with_all[5]
    all_natakhtari = ast.literal_eval(all_natakhtari)
    print(all_natakhtari)
    all_fanta = list_with_all[6]
    all_fanta = ast.literal_eval(all_fanta)
    print(all_fanta)
    all_milkis = list_with_all[7]
    all_milkis = ast.literal_eval(all_milkis)
    print(all_milkis)
    text = 'В вашем заказе:\n'
    if len(all_cocacola) != 0:
        lenght = len(all_cocacola)
        text = text + ' --<code>cola  !:</code>\n'
        num = 1
        for item in list(dict.fromkeys(all_cocacola)):
            num = all_cocacola.count(item)
            text = text + f'{item} x{num}\n'
            lenght = lenght - num
            if lenght == 0:
                break
    if len(all_pepsicola) != 0:
        lenght = len(all_cocacola)
        text = text + ' --<code>pepsi!:</code>\n'
        for item in list(dict.fromkeys(all_pepsicola)):
            num = all_pepsicola.count(item)
            text = text + f'{item} x{num}\n'
            lenght = lenght - num
            if lenght == 0:
                break
    if len(all_sprite) != 0:
        lenght = len(all_sprite)
        text = text + ' --<code>sprite!:</code>\n'
        for item in list(dict.fromkeys(all_sprite)):
            num = all_sprite.count(item)
            text = text + f'{item} x{num}\n'
            lenght = lenght - num
            if lenght == 0:
                break
    if len(all_pulpy) != 0:
        lenght = len(all_pulpy)
        text = text + ' --<code>pulpy !:</code>\n'
        for item in list(dict.fromkeys(all_pulpy)):
            num = all_pulpy.count(item)
            text = text + f'{item} x{num}\n'
            lenght = lenght - num
            if lenght == 0:
                break
    if len(all_crush) != 0:
        lenght = len(all_crush)
        text = text + ' --<code>crush!:</code>\n'
        for item in list(dict.fromkeys(all_crush)):
            num = all_crush.count(item)
            text = text + f'{item} x{num}\n'
            lenght = lenght - num
            if lenght == 0:
                break
    if len(all_natakhtari) != 0:
        lenght = len(all_natakhtari)
        text = text + ' --<code>natakhtari!:</code>\n'
        for item in list(dict.fromkeys(all_natakhtari)):
            num = all_natakhtari.count(item)
            item = int(item)
            text = text + f'{drinks["natakhtari"][0][item]} x{num}\n'
            lenght = lenght - num
            if lenght == 0:
                break
    if len(all_fanta) != 0:
        lenght = len(all_fanta)
        text = text + ' --<code>fanta !:</code>\n'
        for item in list(dict.fromkeys(all_fanta)):
            num = all_fanta.count(item)
            item = int(item)
            text = text + f'{drinks["fanta"][0][item]} x{num}\n'
            lenght = lenght - num
            if lenght == 0:
                break
    if len(all_milkis) != 0:
        lenght = len(all_milkis)
        text = text + ' --<code>milkis !:</code>\n'
        for item in list(dict.fromkeys(all_milkis)):
            num = all_milkis.count(item)
            text = text + f'{item} x{num}\n'
            lenght = lenght - num
            if lenght == 0:
                break
    return text

def get_adr(id):
    try:
        conn = sqlite3.connect('db.db')
        q = conn.cursor()
        result = q.execute('SELECT * FROM adresses WHERE id IS '+str(id)).fetchone()
        result = result[1]
        conn.close()
        return result
    except:
        return None

def insert_adr(message):
    id = message.from_user.id
    conn = sqlite3.connect('db.db')
    q = conn.cursor()
    try:
        q.execute('DELETE FROM adresses WHERE id IS '+str(id))
        conn.commit()
    except:
        pass
    q.execute('INSERT INTO adresses VALUES (?,?)',(id,message.text))
    conn.commit()
    conn.close()

def return_qiwi_link(id):
    conn = sqlite3.connect('db.db')
    q = conn.cursor()
    result = q.execute('SELECT * FROM check_payment WHERE id IS '+str(id)).fetchone()
    tuple = result
    amount = tuple[1]
    code = tuple[2]
    link = f'https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={num_qiwi}&amountInteger={amount}&amountFraction=0&extra%5B%27comment%27%5D={code}&currency=643&blocked[0]=account'
    return link