from flask import Flask, request, jsonify, redirect, send_file
import random
import string
import datetime
import sqlite3
from datetime import datetime, timedelta, date

app = Flask(__name__)
key = 0
UPLOAD_FOLDER = '/send'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def admin_generate_key(days, person):
  print(1)
  try:
      key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
      today = date.today()
      expiration_date = today + timedelta(days=days)
      connection = sqlite3.connect('database.db')
      cursor = connection.cursor()
      last_id = cursor.execute('SELECT MAX(id) FROM keys').fetchone()[0]
      if last_id is None:
          last_id = 0
      else:
          last_id += 1
      print(2)
      cursor.execute("""
          INSERT INTO keys (id, key, time, hwid, person) 
          VALUES (?, ?, ?, ?, ?)
          """, (last_id + 1, key, expiration_date, '', int(person)))
      connection.commit()
      connection.close()
      print(3)
      print(key)
      return {"success": True, "status": True, 'key': key}

  except:
      return {"success": True, "status": False}

def add_days_to_date(input_date, days_to_add):
    input_datetime = datetime.strptime(input_date, '%Y-%m-%d')
    new_datetime = input_datetime + timedelta(days=days_to_add)
    new_date_formatted = new_datetime.strftime('%Y-%m-%d')
    return new_date_formatted

def add_user_to_db(tg_id, product, days):
  try:
      conn = sqlite3.connect('database.db')
      cursor = conn.cursor()
      row = cursor.execute("SELECT * FROM users WHERE tg_id=?", (int(tg_id),))
      for i in row:
        if i[4] == product:
          print(i[3])
          expiration_date = add_days_to_date(str(i[3]), int(days))

          cursor.execute(f"UPDATE users SET time = ? WHERE id = ?", (expiration_date, i[0]))
          conn.commit()
          return {"success": True, "status": True}
      last_id = cursor.execute('SELECT MAX(id) FROM users').fetchall()[0]
      cursor.execute("""INSERT INTO users (id, hwid, tg_id, time, product)
        VALUES (?, ?, ?, ?, ?)
      """, (last_id[0] + 1, 'None', int(tg_id), add_days_to_date(str(date.today().strftime("%Y-%m-%d")), int(days)), product))
      conn.commit()
      return {"success": True, "status": True}

  except:
      return {"success": True, "status": False}


def add_block_users(tg_id):
    try:
        with open("block_users.txt") as f:
            sp = []
            for k in f:
                sp.append(k.replace("\n", ''))
        if str(tg_id) in sp:
            return {"success": True, "status": False}
        else:
            with open("block_users.txt", 'a') as f:
                f.write(f'{tg_id}\n')
                print(1)
                return {"success": True, "status": True}

    except:
        return {"success": True, "status": False}

def add_block_hwid(hwid):
    try:
        with open("block_hwid.txt") as f:
            sp = []
            for k in f:
                sp.append(k.replace("\n", ''))
        if str(hwid) in sp:
            return {"success": True, "status": False}
        else:
            with open("block_hwid.txt", 'a') as f:
                f.write(f'{hwid}\n')
                return {"success": True, "status": True}
    except:
        return {"success": True, "status": False}


def add_days_to_key(days, key):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM keys WHERE key=?", (key,)).fetchone()
        expiration_date = add_days_to_date(str(row[2]), int(days))
        cursor.execute(f"UPDATE keys SET time = ? WHERE key = ?", (expiration_date, key))
        conn.commit()
        return {"success": True, "status": True}

    except:
        return {"success": True, "status": False}


def delete_key(key):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM keys WHERE key = ?", (key,))
        conn.commit()
        conn.close()
        return {"success": True, "status": True}
    except:
        return {"success": True, "status": False}

def add_hwid_to_txt(hwid, data):
    with open("hwid.txt") as file:
        sp = []
        for i in file:
            sp.append(i.replace("\n", ''))
    if hwid not in sp:
        f = open("hwid.txt", "a")
        f.write(f"{hwid}\n")
        f.close()
        return {"success": True, "status": "ask"}
    else:
        with open("block_hwid.txt") as file:
            for i in file:
                if i == hwid:
                    return {"success": True, "status": "Block"}

    f = check_in_keys(hwid=hwid)
    if f[0] == True:
        return {"success": True, "status": True, 'days': f[1]}
    else:
        f = data.get('product')
        f = f.split(".")
        print(f)
        return check_in_tg(hwid=hwid, product=f[0])




def check_in_keys(hwid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM keys").fetchall()
    for i in row:
        if hwid in i[3].split(' '):
            target_date = datetime.strptime(i[2], '%Y-%m-%d')
            current_date = datetime.now()
            delta = target_date - current_date
            days_remaining = delta.days
            if days_remaining > 0:
                return [True, days_remaining]
            else:
                return [False]
    else:
        return [False]

def check_in_tg(hwid, product):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM users WHERE hwid=?", (hwid,)).fetchall()
    print(row)
    for i in row:
        if hwid == i[1] and product == i[4]:
            target_date = datetime.strptime(i[3], '%Y-%m-%d')
            current_date = datetime.now()
            delta = target_date - current_date
            days_remaining = delta.days
            if days_remaining > 0:
                return {"success": True, "status": True, 'days': days_remaining}
            else:
                return {"success": True, "status": "ask"}
    return {"success": True, "status": "ask"}


def add_user_as_tg(tg_id, hwid, prod):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM users WHERE tg_id=? AND product=?", (int(tg_id), prod)).fetchone()
    if row:
        if row[1] == "None":
            cursor.execute("UPDATE users SET hwid=? WHERE tg_id=? AND product=?",
                           (hwid, int(tg_id), prod))
            conn.commit()
            target_date = datetime.strptime(row[3], '%Y-%m-%d')
            current_date = datetime.now()
            delta = target_date - current_date
            days_remaining = delta.days
            days_remaining += 1
            if not(days_remaining >= 0):
                return {"success": True, "status": False, 'message': 'Подписка уже истекла'}

            else:
                return {"success": True, "status": True, 'message': f"Авторизация прошла успешно, дней до окончания - {days_remaining}"}

        else:
            return {"success": True, "status": False, "message": 'Этот tg_id уже занят другим hwid'}
    else:
        return {"success": True, "status": False, "message": 'Tg_id не найден'}


def add_as_key(hwid, key):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    row = cursor.execute(("SELECT * FROM keys WHERE key = ?"),(key,)).fetchone()
    print(row)
    persone = row[4]
    f = row[3]
    f = f.split()
    if len(f) < persone:
        s = ''
        if hwid not in f:
            if len(f) != 0:
                for i in f:
                    s += f'{i} '
            s += f'{hwid} '
            cursor.execute("UPDATE keys SET hwid=? WHERE key = ?",(s, key))
            conn.commit()
            target_date = datetime.strptime(row[2], '%Y-%m-%d')
            current_date = datetime.now()
            delta = target_date - current_date
            days_remaining = delta.days
            days_remaining += 1
            return {"success": True, "status": True, 'message': f"Авторизация прошла успешно, дней до окончания - {days_remaining}"}

        else:
            return {"success": True, "status": False,
                    'message': f"Вы уже подключены к этому ключу"}

    else:
        return {"success": True, "status": False, 'message': 'В ключе уже максимальное количествое пользователей'}




@app.route("/api/v1/messages", methods=["POST"])
def send_message():
    data = request.get_json()
    print(data)
    if data.get("from") == "admin":
        if data.get('do') == 'generate_key':
            response = admin_generate_key(days=int(data.get('days')), person=data.get('person'))
            return jsonify(response)

        elif data.get('do') == 'block_user':
            response = add_block_users(data.get('id_user'))
            return jsonify(response)

        elif data.get('do') == 'block_hwid':
            response = add_block_hwid(data.get('hwid_user'))
            return jsonify(response)

        elif data.get('do') == 'add_day_to':
            response = add_days_to_key(days=data.get('day_to_add'), key=data.get('key'))
            return jsonify(response)

        elif data.get('do') == 'delete_key':
            response = delete_key(data.get('key'))
            return jsonify(response)
    elif data.get('from') == 'user_from_bot':
        response = add_user_to_db(data.get('telegramm_id'), data.get('product'), data.get('days'))
        return jsonify(response)
    elif data.get('from') == 'user':
        response = add_hwid_to_txt(hwid=data.get("hwid"), data=data)
        print(response)
        return jsonify(response)
    elif data.get('from') == 'user_as_key':
        response = add_as_key(hwid=data.get('hwid'), key=data.get('key'))
        return jsonify(response)


    elif data.get('from') == 'user_as_add_tg_id':
        product = data.get('product')
        pd = product.split('.')
        response = add_user_as_tg(hwid=data.get('hwid'), prod=pd[0], tg_id=data.get('telegramm_id'))
        return jsonify(response)



    response = {"success": True, "status": True}
    return jsonify(response)

@app.route('/download/<user_id>')
def download(user_id):
    print(user_id)
    file_path = 'send/pososi.txt'
    return send_file(file_path, as_attachment=True)


@app.route('/')
def hello():
    return """Hello world"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)