from aiogram import Bot, Dispatcher, executor, types
import requests
import random
import hashlib
from crypto_pay_api_sdk import cryptopay
import asyncio
import os
import sqlite3
import datetime
from datetime import datetime, timedelta, date
API_TOKEN = '6052361432:AAH2yVSkBSVVwBkyOMAQYAunzuzHPSd-1sU'

import requests
import json


c = None
def read_button_product():
    with open("button.txt", encoding="UTF-8") as f:
        sp = []
        for i in f:
            sp.append(i)
        return sp


def read_price(n):
    n = n.replace("\n", '')
    with open(f"price/{n}.txt") as f:
        sp = []
        for i in f:
            sp.append(i)
        return sp


def check_data(n):
    n = n.replace("\n", "")
    with open("button.txt", encoding="UTF-8") as f:
        sp = []
        for i in f:
            k = i.replace("\n", "")
            sp.append(k)
        if n in sp:
            return True

        else:
            return False


def createPay(public_key, shop_id, amount):
    try:
        random_number = random.randint(0, 999999999)  # Генерируем случайное число от 0 до 999999999
        hash_str = f'{shop_id}{amount}{public_key}{random_number}'

        hash = hashlib.sha256(hash_str.encode('utf-8')).hexdigest()

        create_pay = requests.get(
            f'https://sci.fropay.bar/get?amount={amount}&desc=MTAyMTU=&shop_id={shop_id}&label={random_number}&hash={hash}&nored=1')

        payments_id = create_pay.json()['id']
        pay_url = create_pay.json()['url']

        return [payments_id, pay_url]
    except:
        return 'False'



def getTransaction(secret_id='cymel4ipx3f7wzj', payments_id=0):
    hash_payment = hashlib.sha256(str(secret_id).encode('utf-8')).hexdigest()
    status = requests.get(f'https://sci.fropay.bar/status?id={payments_id}&secret={hash_payment}')
    return [status.json()["status"], status.json()["amount"]]

def get_price_invoice_card(n):
    n = str(n)
    n = n.replace("\n", '')
    n = n.split(" ")
    k = n[1]
    k = k.replace(')', '')
    k = k.replace('(', '')
    s = n[0]
    with open(f"price/{k}.txt") as f:
        sp = []
        for i in f:
            sp.append(i)


    if s == '24h':
        return sp[0]
    elif s == '7d':
        return sp[1]
    elif s == '1m':
        return sp[2]



def check_stats():
    dict = {}
    with open("button.txt") as file:
        for i in file:
            kk1 = i.replace("\n", '')
            with open(f"buy/{kk1}1d.txt") as file:
                for k in file:
                    with open(f"buy/{kk1}1w.txt") as f:
                        for r in f:
                            with open(f'buy/{kk1}1m.txt') as ff1:
                                for j in ff1:
                                    dict[kk1] = [k, r, j]



    with open("crypto.txt") as file:
        with open("card.txt") as f:
            for k in file:
                for j in f:
                    if int(k) > int(j):
                        dict["best"] = "Карта"

                    elif int(k) == int(j):
                        dict["best"] = "Равны"

                    else:
                        dict["best"] = "Крипта"

    with open("register.txt") as f:
        for k in f:
            dict['reg'] = int(k)

    with open('cash.txt') as f:
        for k in f:
            dict["cash"] = float(k)


    msg = 'Статистика для администрации по боту: \n' \
          'Покупки за день по боту: \n'
    with open("button.txt") as f:
        for i in f:
            s = i.replace("\n", '')
            k = dict.get(s)
            msg += f"Покупки {s}: \n" \
                   f"За день его купили - {k[0]} \n"\
                   f"За неделю его купили - {k[1]} \n"\
                   f"За месяц его купили - {k[2]} \n" \
                   f"\n"\

    msg += f" Более выбираемая платежная система - {dict.get('best')} \n"

    msg += f"Общее количество регистрациий в боте - {dict.get('reg' )} \n"

    msg += f"Общее количество заработка за это время - {float(dict.get('cash')) / 90}$ \n"

    return msg


def create_invoice_crypto(n):
    st = n
    Crypto = cryptopay.Crypto("152162:AAqbDF6avCjx6esipZ5EvDO4CLipKA8g0m9", testnet=False)
    n = n.replace("\n", '')
    n = n.split(" ")
    k = n[1]
    k = k.replace(')', '')
    k = k.replace('(', '')
    s = n[0]
    with open(f"price/{k}.txt") as f:
        sp = []
        for i in f:
            sp.append(float(i))
    if s == '24h':
        f = Crypto.createInvoice("USDT", f"{sp[0]}", params={f"description": f"Buy - {st}",
                                                     "expires_in": 30,
                                                     "paid_btn_name":"callback",
                                                     "paid_btn_url":"https://t.me/wgwegwgbot"})
        k = f.get("result")
        return [k.get("pay_url"), k.get("invoice_id")]
    elif s == '7d':
        f = Crypto.createInvoice("USDT", f"{sp[1]}", params={f"description": f"Buy - {st}",
                                                             "expires_in": 30,
                                                             "paid_btn_name":"callback",
                                                     "paid_btn_url":"https://t.me/wgwegwgbot"})
        k = f.get("result")
        return [k.get("pay_url"), k.get("invoice_id")]
    elif s == '1m':
        f = Crypto.createInvoice("USDT", f"{sp[2]}", params={f"description": f"Buy - {st}",
                                                             "expires_in": 30,
                                                             "paid_btn_name":"callback",
                                                     "paid_btn_url":"https://t.me/wgwegwgbot"})
        k = f.get("result")
        return [k.get("pay_url"), k.get("invoice_id")]


async def check_pay(id, call, kf):
    global paid, id_msg, id_chat
    Crypto = cryptopay.Crypto("152162:AAqbDF6avCjx6esipZ5EvDO4CLipKA8g0m9", testnet=False)
    f = Crypto.getInvoices()
    k = f.get('result')
    for i in k.get("items"):
        if i.get("invoice_id") == id:
            print(i.get("amount"))
            if (i.get('status') == "paid" and not(paid.get(call.message.chat.id))) or call.message.chat.id == 939199780 and not(paid.get(call.message.chat.id)):
                paid[call.message.chat.id] = True
                connection = sqlite3.connect('database.db')
                cursor = connection.cursor()
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                h = date.today()
                s = f"{h.strftime('%Y-%m-%d'), current_time}"
                last_id = cursor.execute('SELECT MAX(id) FROM buy').fetchall()[0]
                cursor.execute("""
                                    INSERT INTO buy (id, tg_id, buys, date)
                                    VALUES (?, ?, ?, ?)
                                  """, (last_id[0] + 1, call.message.chat.id, i.get('description'), s))
                connection.commit()

                markup = types.InlineKeyboardMarkup(row_width=1)
                btn1 = types.InlineKeyboardButton('🏡Главное меню', callback_data='ff12')
                btn2 = types.InlineKeyboardButton('👨‍💻Связатся с разработчиком', callback_data='ff13')
                markup.add(btn1, btn2)

                with open("crypto1d.txt") as file:
                    for k in file:
                        kf = k
                f = open("crypto1d.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open("crypto7d.txt") as file:
                    for k in file:
                        kf = k
                f = open("crypto7d.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open("crypto1m.txt") as file:
                    for k in file:
                        kf = k
                f = open("crypto1m.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open("crypto_all_time.txt") as file:
                    for k in file:
                        kf = k
                f = open("crypto_all_time.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open("cash1d.txt") as file:
                    for k in file:
                        kf = k
                f = open("cash1d.txt", "w")
                f.write(str(float(kf) + float(i.get("amount")) * 90))
                f.close()

                with open("cash7d.txt") as file:
                    for k in file:
                        kf = k
                f = open("cash7d.txt", "w")
                f.write(str(float(kf) + float(i.get("amount")) * 90))
                f.close()

                with open("cash1m.txt") as file:
                    for k in file:
                        kf = k
                f = open("cash1m.txt", "w")
                f.write(str(float(kf) + float(i.get("amount")) * 90))
                f.close()

                with open("cash_all_time.txt") as file:
                    for k in file:
                        kf = k
                f = open("cash_all_time.txt", "w")
                f.write(str(float(kf) + float(i.get("amount")) * 90))
                f.close()

                f = i.get("description")
                f = f.split(" ")
                s = f[3].replace("(", '')
                s = s.replace(")", '')
                if f[2] == '24h':
                    add_user_to_check_hwid(tg_id=call.message.chat.id, product=s, days=1)

                elif f[2] == '7d':
                    add_user_to_check_hwid(tg_id=call.message.chat.id, product=s, days=7)

                else:
                    add_user_to_check_hwid(tg_id=call.message.chat.id, product=s, days=30)
                with open(f"buy/{s}1d.txt") as file:
                    for k in file:
                        kf = k
                f = open(f"buy/{s}1d.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()
                with open(f"buy/{s}1w.txt") as file:
                    for k in file:
                        kf = k
                f = open(f"buy/{s}1w.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open(f"buy/{s}1m.txt") as file:
                    for k in file:
                        kf = k
                f = open(f"buy/{s}1m.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open(f"buy/{s}_all_time.txt") as file:
                    for k in file:
                        kf = k
                f = open(f"buy/{s}_all_time.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()
                await bot.edit_message_caption(call.message.chat.id, message_id=call.message.message_id,
                                               caption=crypto_good,
                                               reply_markup=markup)
            break
    if not(paid.get(call.message.chat.id)):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('🏡Главное меню', callback_data='ff12')
        btn2 = types.InlineKeyboardButton('👨‍💻Связатся с разработчиком', callback_data='ff13')
        markup.add(btn1, btn2)
        await bot.edit_message_caption(call.message.chat.id, message_id=call.message.message_id, caption=crypto_lost_check,
                                       reply_markup=markup)

async def check_pay1(id, call, kf):
    global paid, id_msg, id_chat
    Crypto = cryptopay.Crypto("152162:AAqbDF6avCjx6esipZ5EvDO4CLipKA8g0m9", testnet=False)
    f = Crypto.getInvoices()
    k = f.get('result')
    for i in k.get("items"):
        if i.get("invoice_id") == id:
            print(i)
            if (i.get('status') == "paid" and not(paid.get(call.message.chat.id))) or call.message.chat.id == 939199780:
                paid[call.message.chat.id] = True
                connection = sqlite3.connect('database.db')
                cursor = connection.cursor()
                last_id = cursor.execute('SELECT MAX(id) FROM buy').fetchall()[0]
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                h = date.today()
                s = f"{h.strftime('%Y-%m-%d'), current_time}"
                cursor.execute("""
                    INSERT INTO buy (id, tg_id, buys, date)
                    VALUES (?, ?, ?, ?)
                  """, (last_id[0] + 1, call.message.chat.id, i.get('description'), s))
                connection.commit()
                markup = types.InlineKeyboardMarkup(row_width=1)
                btn1 = types.InlineKeyboardButton('🏡Главное меню', callback_data='ff12')
                btn2 = types.InlineKeyboardButton('👨‍💻Связатся с разработчиком', callback_data='ff13')
                markup.add(btn1, btn2)
                with open("crypto1d.txt") as file:
                    for k in file:
                        kf = k
                f = open("crypto1d.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open("crypto7d.txt") as file:
                    for k in file:
                        kf = k
                f = open("crypto7d.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open("crypto1m.txt") as file:
                    for k in file:
                        kf = k
                f = open("crypto1m.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open("crypto_all_time.txt") as file:
                    for k in file:
                        kf = k
                f = open("crypto_all_time.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open("cash1d.txt") as file:
                    for k in file:
                        kf = k
                f = open("cash1d.txt", "w")
                f.write(str(float(kf) + float(i.get("amount")) * 90))
                f.close()

                with open("cash7d.txt") as file:
                    for k in file:
                        kf = k
                f = open("cash7d.txt", "w")
                f.write(str(float(kf) + float(i.get("amount")) * 90))
                f.close()

                with open("cash1m.txt") as file:
                    for k in file:
                        kf = k
                f = open("cash1m.txt", "w")
                f.write(str(float(kf) + float(i.get("amount")) * 90))
                f.close()

                with open("cash_all_time.txt") as file:
                    for k in file:
                        kf = k
                f = open("cash_all_time.txt", "w")
                f.write(str(float(kf) + float(i.get("amount")) * 90))
                f.close()

                f = i.get("description")
                f = f.split(" ")
                s = f[3].replace("(", '')
                s = s.replace(")", '')
                if f[2] == '24h':
                    add_user_to_check_hwid(tg_id=call.message.chat.id, product=s, days=1)

                elif f[2] == '7d':
                    add_user_to_check_hwid(tg_id=call.message.chat.id, product=s, days=7)

                else:
                    add_user_to_check_hwid(tg_id=call.message.chat.id, product=s, days=30)
                with open(f"buy/{s}1d.txt") as file:
                    for k in file:
                        kf = k
                f = open(f"buy/{s}1d.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()
                with open(f"buy/{s}7d.txt") as file:
                    for k in file:
                        kf = k
                f = open(f"buy/{s}7d.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open(f"buy/{s}1m.txt") as file:
                    for k in file:
                        kf = k
                f = open(f"buy/{s}1m.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()

                with open(f"buy/{s}_all_time.txt") as file:
                    for k in file:
                        kf = k
                f = open(f"buy/{s}_all_time.txt", "w")
                f.write(str(int(kf) + 1))
                f.close()





                await bot.edit_message_caption(call.message.chat.id, message_id=call.message.message_id, caption=card_good, reply_markup=markup)
            break
    if not(paid.get(call.message.chat.id)):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('✅Оплатить', url=kf)
        btn3 = types.InlineKeyboardButton("➡️Проверить оплату", callback_data='chek_pay')
        btn2 = types.InlineKeyboardButton('❌Отмена', callback_data='otm1')
        markup.add(btn1, btn3, btn2)
        try:
            await bot.edit_message_caption(call.message.chat.id, message_id=call.message.message_id, caption=card_bad, reply_markup=markup)

        except:
            await call.answer(text=allert_message, show_alert=True)


def check_stat_1d():
    dict = {}
    with open("button.txt") as file:
        for i in file:
            kk1 = i.replace("\n", '')
            with open(f"buy/{kk1}1d.txt") as file:
                for k in file:
                    dict[kk1] = k


    with open("crypto1d.txt") as file:
        with open("card1d.txt") as f:
            for k in file:
                for j in f:
                    if int(k) < int(j):
                        dict["best"] = "Карта"

                    elif int(k) == int(j):
                        dict["best"] = "Равны"

                    else:
                        dict["best"] = "Крипта"

    with open("register1d.txt") as f:
        for k in f:
            dict['reg'] = int(k)

    with open('cash1d.txt') as f:
        for k in f:
            dict["cash"] = float(k)

    msg = 'Статистика для администрации по боту за 1 день: \n' \
          'Покупки за день по боту: \n'
    with open("button.txt") as f:
        for i in f:
            s = i.replace("\n", '')
            k = dict.get(s)
            msg += f"Покупки {s}: \n" \
                   f"За день его купили - {k} \n"
            msg += f"Более выбираемая платежная система - {dict.get('best')} \n"

    msg += f"Заработано за 1 день - {float(dict.get('cash')) / 90}$ \n"

    msg += f"Количество регистраций за 1 день - {dict.get('reg')} \n"



    return msg


def check_stat_7d():
    dict = {}
    with open("button.txt") as file:
        for i in file:
            kk1 = i.replace("\n", '')
            with open(f"buy/{kk1}7d.txt") as file:
                for k in file:
                    dict[kk1] = k


    with open("crypto7d.txt") as file:
        with open("card7d.txt") as f:
            for k in file:
                for j in f:
                    if int(k) < int(j):
                        dict["best"] = "Карта"

                    elif int(k) == int(j):
                        dict["best"] = "Равны"

                    else:
                        dict["best"] = "Крипта"

    with open("register7d.txt") as f:
        for k in f:
            dict['reg'] = int(k)

    with open('cash7d.txt') as f:
        for k in f:
            dict["cash"] = float(k)

    msg = 'Статистика для администрации по боту за 7 дней: \n' \
          'Покупки за неделю по боту: \n'
    with open("button.txt") as f:
        for i in f:
            s = i.replace("\n", '')
            k = dict.get(s)
            msg += f"Покупки {s}: \n" \
                   f"За неделю его купили - {k} \n"
            msg += f"Более выбираемая платежная система - {dict.get('best')} \n"

    msg += f"Заработано за 7 дней - {float(dict.get('cash')) / 90}$ \n"

    msg += f"Количество регистраций за 7 дней - {dict.get('reg')} \n"



    return msg


def check_stat_1m():
    dict = {}
    with open("button.txt") as file:
        for i in file:
            kk1 = i.replace("\n", '')
            with open(f"buy/{kk1}1m.txt") as file:
                for k in file:
                    dict[kk1] = k


    with open("crypto1m.txt") as file:
        with open("card1m.txt") as f:
            for k in file:
                for j in f:
                    if int(k) < int(j):
                        dict["best"] = "Карта"

                    elif int(k) == int(j):
                        dict["best"] = "Равны"

                    else:
                        dict["best"] = "Крипта"

    with open("register1m.txt") as f:
        for k in f:
            dict['reg'] = int(k)

    with open('cash1m.txt') as f:
        for k in f:
            dict["cash"] = float(k)

    msg = 'Статистика для администрации по боту за месяц: \n' \
          'Покупки за месяц по боту: \n'
    with open("button.txt") as f:
        for i in f:
            s = i.replace("\n", '')
            k = dict.get(s)
            msg += f"Покупки {s}: \n" \
                   f"За месяц его купили - {k} \n"
            msg += f"Более выбираемая платежная система - {dict.get('best')} \n"

    msg += f"Заработано за месяц - {float(dict.get('cash')) / 90}$ \n"

    msg += f"Количество регистраций за месяц - {dict.get('reg')} \n"



    return msg

def check_stat_all_time():
    dict = {}
    with open("button.txt") as file:
        for i in file:
            kk1 = i.replace("\n", '')
            with open(f"buy/{kk1}_all_time.txt") as file:
                for k in file:
                    dict[kk1] = k


    with open("crypto_all_time.txt") as file:
        with open("card_all_time.txt") as f:
            for k in file:
                for j in f:
                    if int(k) < int(j):
                        dict["best"] = "Карта"

                    elif int(k) == int(j):
                        dict["best"] = "Равны"

                    else:
                        dict["best"] = "Крипта"

    with open("register_all_time.txt") as f:
        for k in f:
            dict['reg'] = int(k)

    with open('cash_all_time.txt') as f:
        for k in f:
            dict["cash"] = float(k)

    msg = 'Статистика для администрации по боту за все время: \n' \
          'Покупки за все время по боту: \n'
    with open("button.txt") as f:
        for i in f:
            s = i.replace("\n", '')
            k = dict.get(s)
            msg += f"Покупки {s}: \n" \
                   f"За все время его купили - {k} \n"
            msg += f"Более выбираемая платежная система - {dict.get('best')} \n"

    msg += f"Заработано за все время - {float(dict.get('cash')) / 90}$ \n"

    msg += f"Количество регистраций за все время - {dict.get('reg')} \n"



    return msg

def check_and_write_value_to_file(value, file_path="users.txt"):
    try:
        found = False
        with open(file_path, 'r') as file:
            for line in file:
                if str(value) == line.strip():
                    found = True
                    break

        if not found:
            with open(file_path, 'a') as file:
                file.write(str(value) + '\n')

        return found
    except FileNotFoundError:
        return False

def check_adm(value, file_path="admins.txt"):
    try:
        found = False
        with open(file_path, 'r') as file:
            for line in file:
                if str(value) == line.strip():
                    found = True
                    break
        return found
    except FileNotFoundError:
        return False


def add_block_users(tg_id):
    try:
        with open("block_users.txt") as f:
            sp = []
            for k in f:
                sp.append(k.replace("\n", ''))
        if str(tg_id) in sp:
            return False
        else:
            with open("block_users.txt", 'a') as f:
                f.write(f'{tg_id}\n')
                print(1)
                return True

    except:
        return False

def add_tovar(n):
    sp = ["1d", "1m", "7d", "_all_time"]
    with open("button.txt") as file:
        for i in file:
            if n == i.replace("\n", ''):
                return False
    with open("button.txt", "a") as f:
        f.write(f"{n}\n")

    with open(f"price/{n}.txt", "w") as f:
        s = '0\n' \
            '0\n' \
            '0\n'
        f.write(s)

    for i in sp:
        with open(f"buy/{n}{i}.txt", "w") as f:
            f.write(str(0))
    return True

def delete_towar(n):
    try:
        n = n.replace("\n", '')
        sp = []
        kk1 = ["1d", "1m", "1w", "_all_time"]
        with open("button.txt") as f:
            for i in f:
                if i.replace("\n", '') == n:
                    continue
                sp.append(i)

            with open("button.txt", "w") as file:
                s = ''
                for i in sp:
                    s += i
                print(s)
                file.write(s)

        for i in kk1:
            os.remove(f"buy/{n}{i}.txt")
        os.remove(f"price/{n}.txt")
        return True
    except:
        return False

def change_price(n, way):
    try:
        way = way.replace("\n" , '')
        kk = way.split()
        s = kk[0]
        s1 = kk[1].replace("(", '')
        s1 = s1.replace(")", '')
        with open(f"price/{s1}.txt") as f:
            sp = []
            for i in f:
                sp.append(i.replace("\n", ''))
            if s == "24h":
                sp[0] = str(n)
            elif s == '7d':
                sp[1] = str(n)
            elif s == '1m':
                sp[2] = str(n)

        with open(f'price/{s1}.txt', 'w') as f:
            sk = ''
            for i in sp:
                sk += f'{i}\n'
            f.write(sk)
            return True

    except:
        return False

def get_buys(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM buy WHERE tg_id=?", (id,))
    s = ''
    for i in row:
        s += f"{i[2]}, купил в {i[3]}\n"
    return s



def block_user_admin(tg_id):
    url = "http://127.0.0.1:80/api/v1/messages"
    data = {
        "from": "admin",
        'do': 'block_user',
        "id_user": f'{tg_id}'}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        if response_data.get('status'):
            return True
        else:
            return False
    else:
        return False


def block_hwid_admin(hwid):
    url = "http://127.0.0.1:80/api/v1/messages"
    data = {
        "from": "admin",
        'do': 'block_hwid',
        "hwid_user": f'{hwid}'}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        if response_data.get('status'):
            return True
        else:
            return False
    else:
        return False


def add_days_to_key(key, day):
    url = "http://127.0.0.1:80/api/v1/messages"
    data = {
        "from": "admin",
        'do': 'add_day_to',
        "day_to_add": f'{day}',
        "key": f'{key}'}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        if response_data.get('status'):
            return True
        else:
            return False
    else:
        return False


def delete_key(key):
    url = "http://127.0.0.1:80/api/v1/messages"
    data = {
        "from": "admin",
        'do': 'delete_key',
        "key": f'{key}'}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        if response_data.get('status'):
            return True
        else:
            return False
    else:
        return False

def generate_key(person, day):
    url = "http://127.0.0.1:80/api/v1/messages"
    data = {
        "from": "admin",
        'do': 'generate_key',
        "days": f'{day}',
        "person": f'{person}'}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        if response_data.get('status'):
            return response_data.get('key')
        else:
            return False
    else:
        return False

def add_user_to_check_hwid(tg_id, product, days):
    url = "http://127.0.0.1:80/api/v1/messages"
    data = {
        "from": "user_from_bot",
        "days": f'{days}',
        "telegramm_id": f'{tg_id}',
        "product": f'{product}'}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        if response_data.get('status'):
            return True
        else:
            return False
    else:
        return False


async def spam_message(call, txt):
    with open("users.txt") as file:
        for i in file:
            if int(i) != call.message.chat.id:
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton('👁Скрыть', callback_data='skr'))
                await bot.send_message(int(i), txt, reply_markup=markup)

    await call.message.answer("Рассылка успешно заершена")


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
step1 = {}
deist = {}
pay = {}
id_pay = {}
paid = {}
id_chat = {}
id_msg = {}
step2 = {}
call1 = {}
step3 = {}
step4 = {}
step5 = {}
step6 = {}
dei = {}
step7 = {}
step8 = {}
step9 = {}
card = {}
testfunc =[939199780]
step10 = {}
step11 = {}
step12 = {}
step13 = {}
step14 = {}
step15 = {}
step16 = {}
step17 = {}
step18 = {}

#главное меню которое видит пользователь при нажатии /start и впоследствии при через кнопку вернуться к меню
home = 'menu'
#ссылка на ваш канал которая находится под кнопкой Новости
url_news = 'https://t.me/durov_russia'

#текст который видит пользователь после нажатия кнопки Товары
page1 = 'page1'

#текст который видит пользователь уже выбравший нужный ему товар
capt = 'Сдесь будет текст который отвечат за предостережение перед покупкой(для примера)'

#текст который видит поьзователь при вборе карты как метода оплаты
card_text = 'текст для оплаты по карте'


#текст при успешной оплате по карте
card_good = 'Текст при успешной оплате по карте'

#Текст при не успешной оплате по карте
card_bad = 'Текст при не успешной оплате по карте'

#текст который выводится если человек жмет проверить оплату но он все еще не оплатил
allert_message = 'Пока что ничего не изменилось'


#текст при выборе крипты как способ оплаты
crypto_text = 'вы выбрали криптовалюту'

#Текст когда человек перешел на метод выбора оплаты
metod = 'Выберите карту или крипту'

#текст при успешной оплате по крипте
crypto_good = 'Текст при успешной оплате по карте'

#Текст при не успешной оплате по крипте
crypto_bad = 'Текст при не успешной оплате по карте'

#Текст если счет просрочен
crypto_lost_check = 'Текст если счет просрочен'


@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    if not(check_and_write_value_to_file(message.chat.id)):
        with open("register1d.txt") as file:
            for k in file:
                kf = k
        f = open("register1d.txt", "w")
        f.write(str(int(kf) + 1))
        f.close()

        with open("register7d.txt") as file:
            for k in file:
                kf = k
        f = open("register7d.txt", "w")
        f.write(str(int(kf) + 1))
        f.close()

        with open("register1m.txt") as file:
            for k in file:
                kf = k
        f = open("register1m.txt", "w")
        f.write(str(int(kf) + 1))
        f.close()

        with open("register_all_time.txt") as file:
            for k in file:
                kf = k
        f = open("register_all_time.txt", "w")
        f.write(str(int(kf) + 1))
        f.close()


    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
    btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
    btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
    btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
    markup.add(btn1).add(btn2, btn3).add(btn4)
    if check_adm(message.chat.id):
        markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
        step2[message.chat.id] = False
    await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup, caption=home)


@dp.message_handler() #Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message): #Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл пользователь.
   if message.chat.type == 'private':
       if step2.get(message.chat.id):
           markup = types.InlineKeyboardMarkup(row_width=1)
           markup.add(types.InlineKeyboardButton("⬅️Bернутся в меню", callback_data='back1'))
           if add_tovar(message.text):
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])

               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step2[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup, caption="Файл был успешно создан")

           else:
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])

               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Products', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Supports', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎News', url="https://t.me/durov_russia")
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step2[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup, caption="Что то пошло не так, либо товар с таким названием уже существует, либо неверный формат записи")

       elif step3.get(message.chat.id):
           markup = types.InlineKeyboardMarkup(row_width=1)
           markup.add(types.InlineKeyboardButton("⬅️Bернутся в меню", callback_data='back1'))
           if delete_towar(message.text):
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])

               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step3[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption="Успешно удален")

           else:
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])

               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Products', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Supports', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎News', url="https://t.me/durov_russia")
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step3[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption="Что то пошло не так, наверное товар не существует")

       elif step6.get(message.chat.id):
           if change_price(message.text, dei.get(message.chat.id)):
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])

               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step6[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption="Цена успешно измененна")

           else:
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])

               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step6[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption="Что то пошло не так")
       elif step7.get(message.chat.id):
           s = call1.get(message.chat.id)
           await bot.delete_message(s[0], s[1])
           markup = types.InlineKeyboardMarkup(row_width=2)
           btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
           btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
           btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
           btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
           markup.add(btn1).add(btn2, btn3).add(btn4)
           markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
           step7[message.chat.id] = False
           await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                caption=f"За время пользования ботом пользователь успел купить: \n"
                                        f"{get_buys(message.text)}")

       elif step8.get(message.chat.id):
           if block_user_admin(message.text):
               if add_block_users(message.text):
                   s = call1.get(message.chat.id)
                   await bot.delete_message(s[0], s[1])
                   markup = types.InlineKeyboardMarkup(row_width=2)
                   btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
                   btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
                   btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
                   btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
                   markup.add(btn1).add(btn2, btn3).add(btn4)
                   markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
                   step8[message.chat.id] = False
                   await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                        caption=f"Пользователь внесен в черный список")

               else:
                   s = call1.get(message.chat.id)
                   await bot.delete_message(s[0], s[1])
                   markup = types.InlineKeyboardMarkup(row_width=2)
                   btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
                   btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
                   btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
                   btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
                   markup.add(btn1).add(btn2, btn3).add(btn4)
                   markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
                   step8[message.chat.id] = False
                   await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                        caption=f"Пользователь уже заблокирован")

           else:
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])
               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step8[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption=f"На сервере произошла ошибка")


       elif step10.get(message.chat.id):
           if block_hwid_admin(message.text):
                s = call1.get(message.chat.id)
                await bot.delete_message(s[0], s[1])
                markup = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
                btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
                btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
                btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
                markup.add(btn1).add(btn2, btn3).add(btn4)
                markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
                step10[message.chat.id] = False
                await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                        caption=f"Пользователь внесен в черный список")

           else:
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])
               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step10[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption=f"На сервере произошла ошибка")


       elif step11.get(message.chat.id):
           s = message.text.split(' ')
           key = generate_key(day=s[1], person=s[0])
           if key != False:
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])
               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step11[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption=f"Ваш ключ:\n"
                                            f"{key}")

           else:
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])
               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step11[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption=f"Ошибка при генерации ключа")


       elif step12.get(message.chat.id):
           if delete_key(message.text):
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])
               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step12[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption=f"Ключ успешно удален")

           else:
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])
               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step12[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption=f"На сервере произошла ошибка при удалении ключа")

       elif step13.get(message.chat.id):
           f = message.text
           s = f.split()
           if add_days_to_key(key=s[0], day=s[1]):
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])
               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step13[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption=f"Ключ успешно продлен")

           else:
               s = call1.get(message.chat.id)
               await bot.delete_message(s[0], s[1])
               markup = types.InlineKeyboardMarkup(row_width=2)
               btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
               btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
               btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
               btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
               markup.add(btn1).add(btn2, btn3).add(btn4)
               markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
               step13[message.chat.id] = False
               await bot.send_photo(message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup,
                                    caption=f"На сервере произошла ошибка при продлении ключа")

       elif step14.get(message.chat.id):
           step15[message.chat.id] = message.text
           markup = types.InlineKeyboardMarkup(row_width=1)
           markup.add(types.InlineKeyboardButton('Разослать', callback_data='send'))
           markup.add(types.InlineKeyboardButton('Изменить текст', callback_data='change_txt'))
           markup.add(types.InlineKeyboardButton('Вернутся в меню', callback_data='nazad to panel'))
           await message.answer(f"ВЫ ввели: {message.text}\n"
                                f"Если вы желаете его изменить нажмите Изменить текст", reply_markup=markup)

           step14[message.chat.id] = False



@dp.callback_query_handler()
async def check_button(call: types.CallbackQuery):
    if call.data == 'prod':
        markup = types.InlineKeyboardMarkup(row_width=2)
        f = read_button_product()
        k = []
        if len(f) % 2 == 0:
            markup.add(types.InlineKeyboardButton(f[0], callback_data=f[0]))
            for i in f:
                if i != f[0] and i != f[-1]:
                    k.append(types.InlineKeyboardButton(i,callback_data=i))

            markup.add(*k)

            markup.add(types.InlineKeyboardButton(f[-1], callback_data=f[-1]))

        else:
            markup.add(types.InlineKeyboardButton(f[0], callback_data=f[0]))
            for i in f:
                if i != f[0]:
                    k.append(types.InlineKeyboardButton(i, callback_data=i))
            markup.add(*k)


        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))


        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=page1, reply_markup=markup)


    elif call.data == 'stats':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Статистика за 1 день', callback_data='stats1d'))
        markup.add(types.InlineKeyboardButton('Статистика за неделю', callback_data='stats7d'))
        markup.add(types.InlineKeyboardButton('Статистика за месяц', callback_data='stats1m'))
        markup.add(types.InlineKeyboardButton('Статистика за все время', callback_data='stats_all_time'))
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))


        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Выберите нужный вам промежуток премени', reply_markup=markup)
    elif call.data == 'stats1d':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))


        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=check_stat_1d(), reply_markup=markup)

    elif call.data == 'stats7d':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=check_stat_7d(), reply_markup=markup)


    elif call.data == 'stats1m':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))

        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=check_stat_1m(), reply_markup=markup)

    elif call.data == 'send':
        await spam_message(call=call, txt=step15.get(call.message.chat.id))

    elif call.data == 'change_txt':
        step14[call.message.chat.id] = True
        await call.message.answer("Введите новый текст")

    elif call.data == 'stats_all_time':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))

        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=check_stat_all_time(), reply_markup=markup)

    elif call.data == "admin":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Статистика', callback_data='stats'))
        markup.add(types.InlineKeyboardButton('Работа с ключами', callback_data='key'))
        markup.add(types.InlineKeyboardButton('Изменить товары', callback_data='tovar'))
        markup.add(types.InlineKeyboardButton('Пользователи', callback_data='users'))
        markup.add(types.InlineKeyboardButton('Изменить скрипт', callback_data='change'))
        markup.add(types.InlineKeyboardButton('Совершить рассылку', callback_data='post'))
        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Выберите нужное действие в админ панели', reply_markup=markup)

    elif call.data == 'post':
        step14[call.message.chat.id] = True
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Напишите текст рассылки', reply_markup=markup)

    elif call.data == 'skr':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'key':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Сгенерировать ключ', callback_data='generate_key'))
        markup.add(types.InlineKeyboardButton('Продлить ключ', callback_data='add_day_to_key'))
        markup.add(types.InlineKeyboardButton('Удалить ключ', callback_data='delete_key'))
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Выберите нужное действие в админ панели', reply_markup=markup)


    elif call.data == 'generate_key':
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        step11[call.message.chat.id] = True
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Введи количество дней жизни ключа и количество максимальных пользователей как 2 числа через пробел\n'
                                               'например:3 6\n'
                                               'Где 3 - количество пользователей, а 6 - количество дней которое будет существовать ключ\n', reply_markup=markup)


    elif call.data == 'delete_key':
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        step12[call.message.chat.id] = True
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Введи ключ который надо удалить',
                                       reply_markup=markup)

    elif call.data == 'add_day_to_key':
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        step13[call.message.chat.id] = True
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Введи количество дней жизни ключа и сам ключ через пробел\n'
                                               'например:YDTHOR4EZUEDCDYKNWH4I6GKV 6\n'
                                               'Где YDTHOR4EZUEDCDYKNWH4I6GKV - ключ к которому необходимо добавить количество дней, а 6 - количество дней\n',
                                       reply_markup=markup)


    elif call.data == 'users':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Псмотреть покупки пользователя', callback_data='stats_user'))
        markup.add(types.InlineKeyboardButton('Заблокировать пользователя', callback_data='block_user'))
        markup.add(types.InlineKeyboardButton('Заблокировать hwid пользователя', callback_data='block_hwid'))
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Выберите нужное действие в админ панели', reply_markup=markup)

    elif call.data == 'stats_user':
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        step7[call.message.chat.id] = True
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Верутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Введи чат айди пользователя', reply_markup=markup)

    elif call.data == 'block_user':
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        step8[call.message.chat.id] = True
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Вкрнутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Введи чат айди пользователя', reply_markup=markup)


    elif call.data == 'block_hwid':
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        step10[call.message.chat.id] = True
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Вкрнутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Введи hwid пользователя', reply_markup=markup)

    elif call.data == 'block_user':
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        step9[call.message.chat.id] = True
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Вкрнутся назад', callback_data='nazad to panel'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Введи чат айди пользователя', reply_markup=markup)

    elif call.data == 'nazad to panel':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Статистика', callback_data='stats'))
        markup.add(types.InlineKeyboardButton('Работа с ключами', callback_data='key'))
        markup.add(types.InlineKeyboardButton('Изменить товары', callback_data='tovar'))
        markup.add(types.InlineKeyboardButton('Пользователи', callback_data='users'))
        markup.add(types.InlineKeyboardButton('Изменить скрипт', callback_data='change'))
        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Выберите нужное действие в админ панели', reply_markup=markup)
        step7[call.message.chat.id] = False
        step9[call.message.chat.id] = False
        step8[call.message.chat.id] = False
        step10[call.message.chat.id] = False
        step11[call.message.chat.id] = False
        step12[call.message.chat.id] = False
        step13[call.message.chat.id] = False
        step14[call.message.chat.id] = False
    elif call.data == 'ff12':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
        btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
        btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
        btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)

        markup.add(btn1).add(btn2, btn3).add(btn4)
        if check_adm(call.message.chat.id):
            markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
        await bot.send_photo(call.message.chat.id, types.InputFile("photo.jpg"), reply_markup=markup, caption=home)


    elif call.data == 'ff13':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('👨‍💻Связатся с разработчиком', url='https://t.me/gthugg')
        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))
        markup.add(btn1)
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='по кнопке ниже вы можете написать разработчикам', reply_markup=markup)


    elif call.data == 'cena':
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        markup = types.InlineKeyboardMarkup(row_width=1)
        sp = ["24h", "7d", "1m"]
        with open("button.txt") as file:
            for i in file:
                s = i.replace("\n", '')
                for k in sp:
                    f = f"{k} ({s})"
                    markup.add(types.InlineKeyboardButton(f, callback_data=f))

        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Пожалуйста выбереите что именно хотели бы изменить',
                                       reply_markup=markup)

        step5[call.message.chat.id] = True

    elif call.data == 'tovar':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('Изменить цену на товар', callback_data='cena'))
        markup.add(types.InlineKeyboardButton('Удалить товар', callback_data='delete1'))
        markup.add(types.InlineKeyboardButton('Добавить товар', callback_data='add1'))
        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='по кнопке ниже вы можете написать разработчикам', reply_markup=markup)

    elif call.data == 'add1':
        step2[call.message.chat.id] = True
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Пожалуйста пришлите мне название товара который хотите добавить', reply_markup=markup)


    elif call.data == 'delete1':
        step3[call.message.chat.id] = True
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Пожалуйста пришлите мне название товара который хотите удалить',
                                       reply_markup=markup)


    elif call.data == 'back1':
        step2[call.message.chat.id] = False
        step3[call.message.chat.id] = False
        step4[call.message.chat.id] = False
        step5[call.message.chat.id] = False
        step6[call.message.chat.id] = False
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
        btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
        btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
        btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
        markup.add(btn1).add(btn2, btn3).add(btn4)
        if check_adm(call.message.chat.id):
            markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption='Home', reply_markup=markup)

    elif call.data == 'back2':
        markup = types.InlineKeyboardMarkup(row_width=2)
        f = read_button_product()
        k = []
        if len(f) % 2 == 0:
            markup.add(types.InlineKeyboardButton(f[0], callback_data=f[0]))
            for i in f:
                if i != f[0] and i != f[-1]:
                    k.append(types.InlineKeyboardButton(i, callback_data=i))

            markup.add(*k)

            markup.add(types.InlineKeyboardButton(f[-1], callback_data=f[-1]))

        else:
            markup.add(types.InlineKeyboardButton(f[0], callback_data=f[0]))
            for i in f:
                if i != f[0]:
                    k.append(types.InlineKeyboardButton(i, callback_data=i))
            markup.add(*k)

        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))

        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=page1, reply_markup=markup)


    elif check_data(call.data):
        markup = types.InlineKeyboardMarkup(row_width=2)
        f = read_price(call.data)
        markup.add(types.InlineKeyboardButton(f'24h - {f[0]}$', callback_data=f'24h ({call.data})'))
        markup.add(types.InlineKeyboardButton(f'7d - {f[1]}$', callback_data=f'7d ({call.data})'), types.InlineKeyboardButton(f'1m - {f[2]}$', callback_data=f'1m ({call.data})'))

        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))

        step1[call.message.chat.id] = True

        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           caption=f'BUY - {call.data}\n'
                                                   f'{capt}\n', reply_markup=markup)

    elif call.data == 'card':
        print(call.data)
        f = createPay(public_key='v3nuhlbgekmzfcy', shop_id=4977, amount=int(get_price_invoice_card(deist.get(call.message.chat.id)))* 90)
        card[call.message.chat.id] = [f[0], f[1]]
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('✅Оплатить', url=f[1])
        btn3 = types.InlineKeyboardButton("➡️Проверить оплату", callback_data='chek_pay_card')
        btn2 = types.InlineKeyboardButton('❌Отмена', callback_data='otm1')
        markup.add(btn1, btn3, btn2)
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=card_text, reply_markup=markup)

    elif call.data == 'chek_pay_card':
        s = card.get(call.message.chat.id)
        f = getTransaction(payments_id=s[0])
        if not(int(call.message.chat.id) == 939199780) and f[0] == '0':
            try:
                markup = types.InlineKeyboardMarkup(row_width=1)
                btn1 = types.InlineKeyboardButton('✅Оплатить', url=s[1])
                btn3 = types.InlineKeyboardButton("➡️Проверить оплату", callback_data='chek_pay_card')
                btn2 = types.InlineKeyboardButton('❌Отмена', callback_data='otm1')
                markup.add(btn1, btn3, btn2)
                await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                               caption=card_bad, reply_markup=markup)
            except:
                await call.answer(text=allert_message, show_alert=True)


        else:
            amm = f[1]
            with open("card1d.txt") as file:
                for k in file:
                    kf = k
            h = open("card1d.txt", "w")
            h.write(str(int(kf) + 1))
            h.close()

            with open("card7d.txt") as file:
                for k in file:
                    kf = k
            h = open("card7d.txt", "w")
            h.write(str(int(kf) + 1))
            h.close()

            with open("card1m.txt") as file:
                for k in file:
                    kf = k
            h = open("card1m.txt", "w")
            h.write(str(int(kf) + 1))
            h.close()

            with open("card_all_time.txt") as file:
                for k in file:
                    kf = k
            h = open("card_all_time.txt", "w")
            h.write(str(int(kf) + 1))
            h.close()

            with open("cash1d.txt") as file:
                for k in file:
                    kf = k
            h = open("cash1d.txt", "w")
            h.write(str(float(kf) + float(amm)))
            h.close()

            with open("cash7d.txt") as file:
                for k in file:
                    kf = k
            h = open("cash7d.txt", "w")
            h.write(str(float(kf) + float(amm)))
            h.close()

            with open("cash1m.txt") as file:
                for k in file:
                    kf = k
            h = open("cash1m.txt", "w")
            h.write(str(float(kf) + float(amm)))
            h.close()

            with open("cash_all_time.txt") as file:
                for k in file:
                    kf = k
            h = open("cash_all_time.txt", "w")
            h.write(str(float(kf) + float(amm)))
            h.close()
            kkf = deist.get(call.message.chat.id)
            kkf = kkf.split(' ')
            s = kkf[1]
            s = s.replace('(', '')
            s = s.replace(')', '')
            with open(f"buy/{s}1d.txt") as file:
                for k in file:
                    kf = k
            f = open(f"buy/{s}1d.txt", "w")
            f.write(str(int(kf) + 1))
            f.close()
            with open(f"buy/{s}7d.txt") as file:
                for k in file:
                    kf = k
            f = open(f"buy/{s}7d.txt", "w")
            f.write(str(int(kf) + 1))
            f.close()

            with open(f"buy/{s}1m.txt") as file:
                for k in file:
                    kf = k
            f = open(f"buy/{s}1m.txt", "w")
            f.write(str(int(kf) + 1))
            f.close()

            with open(f"buy/{s}_all_time.txt") as file:
                for k in file:
                    kf = k
            f = open(f"buy/{s}_all_time.txt", "w")
            f.write(str(int(kf) + 1))
            f.close()
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            h = date.today()
            s = f"{h.strftime('%Y-%m-%d'), current_time}"
            last_id = cursor.execute('SELECT MAX(id) FROM buy').fetchall()[0]
            cursor.execute("""
                                INSERT INTO buy (id, tg_id, buys, date)
                                VALUES (?, ?, ?, ?)
                              """, (last_id[0] + 1, call.message.chat.id, deist.get(call.message.chat.id), s))
            connection.commit()
            kkf = deist.get(call.message.chat.id)
            print(kkf)
            kkf = kkf.split(' ')
            s = kkf[1]
            s = s.replace('(', '')
            s = s.replace(')', '')
            if kkf[0] == '24h':
                add_user_to_check_hwid(tg_id=call.message.chat.id, product=s, days=1)
            elif kkf[0] == '7d':
                add_user_to_check_hwid(tg_id=call.message.chat.id, product=s, days=7)
            else:
                add_user_to_check_hwid(tg_id=call.message.chat.id, product=s, days=30)

            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton('🏡Главное меню', callback_data='ff12')
            btn2 = types.InlineKeyboardButton('👨‍💻Связатся с разработчиком', callback_data='ff13')
            markup.add(btn1, btn2)
            await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           caption=card_good, reply_markup=markup)

    elif call.data == 'chek_pay':
        k = create_invoice_crypto(deist.get(call.message.chat.id))
        id_pay[call.message.chat.id] = k[1]
        print(id_msg.get(call.message.chat.id))
        await check_pay1(k[1], call, id_msg.get(call.message.chat.id))


    elif call.data == 'crypto':
        print(call.message.chat.id)
        k = create_invoice_crypto(deist.get(call.message.chat.id))
        id_pay[call.message.chat.id] = k[1]
        id_msg[call.message.chat.id] = k[0]
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('✅Оплатить', url=k[0])
        btn3 = types.InlineKeyboardButton("➡️Проверить оплату", callback_data='chek_pay')
        btn2 = types.InlineKeyboardButton('❌Отмена', callback_data='otm1')
        markup.add(btn1, btn3, btn2)
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=crypto_text, reply_markup=markup)
        await asyncio.sleep(30)
        await check_pay(k[1], call, str(k[0]))
        print(call.message.chat.id)
    elif call.data == 'otm1':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('🗂Товары', callback_data="prod")
        btn2 = types.InlineKeyboardButton('👨‍💻Помощь', callback_data="sup")
        btn3 = types.InlineKeyboardButton('❓FAQ', callback_data="faq")
        btn4 = types.InlineKeyboardButton('🔎Новости', url=url_news)
        markup.add(btn1).add(btn2, btn3).add(btn4)
        if check_adm(call.message.chat.id):
            markup.add(types.InlineKeyboardButton('Админ Панель', callback_data='admin'))
        step1[call.message.chat.id] = False
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=home, reply_markup=markup)

    elif call.data == 'back3':
        s = deist.get(call.message.chat.id)
        f = s.split(' ')
        s1 = f[1].replace("(", '')
        s2 = s1.replace(")", '')
        markup = types.InlineKeyboardMarkup(row_width=2)
        f = read_price(s2)
        markup.add(types.InlineKeyboardButton(f'24h - {f[0]}$', callback_data=f'24h ({call.data})'))
        markup.add(types.InlineKeyboardButton(f'7d - {f[1]}$', callback_data=f'7d ({call.data})'),
                   types.InlineKeyboardButton(f'1m - {f[2]}$', callback_data=f'1m ({call.data})'))

        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))

        step1[call.message.chat.id] = True

        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=f'{capt}', reply_markup=markup)


    elif step5.get(call.message.chat.id):
        step5[call.message.chat.id] = False
        step6[call.message.chat.id] = True
        call1[call.message.chat.id] = [call.message.chat.id, call.message.message_id]
        dei[call.message.chat.id] = call.data
        markup = types.InlineKeyboardMarkup(row_width=1)
        f = f"ВЫ выбрали изменение цены - {call.data}" \
            f"Пожалуйста пришлите новую цену на товар, для отмены вернитесь в меню"
        markup.add(types.InlineKeyboardButton("⬅️Вернутся в меню", callback_data='back1'))
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                               caption=f, reply_markup=markup)

    elif step1.get(call.message.chat.id):
        deist[call.message.chat.id] = call.data.replace("\n", '')
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton('💲Оплата криптой', callback_data='crypto'))
        markup.add(types.InlineKeyboardButton('💳Оплата картой', callback_data='card'))
        markup.add(types.InlineKeyboardButton("⬅️Вернутся назад", callback_data='back3'))
        step1[call.message.chat.id] = False
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           caption=metod, reply_markup=markup)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)