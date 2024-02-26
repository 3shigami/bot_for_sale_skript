def check_stat_1d():
    dct = {}
    with open("button.txt") as file:
        for i in file:
            kk1 = i.replace("\n", '')
            with open(f"buy/{kk1}1d.txt") as file:
                for k in file:
                    dct[kk1] = k


    with open("crypto1d.txt") as file:
        with open("card1d.txt") as f:
            for k in file:
                for j in f:
                    if int(k) > int(j):
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
            msg += f" Более выбираемая платежная система - {dict.get('best')} \n"

    msg += f"Заработано за 1 день - {float(dict.get('cash')) / 90}$ \n"

    msg += f"Количество регистраций за 1 день - {dict.get('reg')} \n"



    return msg


def check_stat_7d():
    dct = {}
    with open("button.txt") as file:
        for i in file:
            kk1 = i.replace("\n", '')
            with open(f"buy/{kk1}7d.txt") as file:
                for k in file:
                    dct[kk1] = k


    with open("crypto7d.txt") as file:
        with open("card7d.txt") as f:
            for k in file:
                for j in f:
                    if int(k) > int(j):
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
            msg += f" Более выбираемая платежная система - {dict.get('best')} \n"

    msg += f"Заработано за 7 дней - {float(dict.get('cash')) / 90}$ \n"

    msg += f"Количество регистраций за 7 дней - {dict.get('reg')} \n"



    return msg


def check_stat_1m():
    dct = {}
    with open("button.txt") as file:
        for i in file:
            kk1 = i.replace("\n", '')
            with open(f"buy/{kk1}1m.txt") as file:
                for k in file:
                    dct[kk1] = k


    with open("crypto1m.txt") as file:
        with open("card1m.txt") as f:
            for k in file:
                for j in f:
                    if int(k) > int(j):
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
            msg += f" Более выбираемая платежная система - {dict.get('best')} \n"

    msg += f"Заработано за месяц - {float(dict.get('cash')) / 90}$ \n"

    msg += f"Количество регистраций за месяц - {dict.get('reg')} \n"



    return msg


def check_stat_all_time():
    dct = {}
    with open("button.txt") as file:
        for i in file:
            kk1 = i.replace("\n", '')
            with open(f"buy/{kk1}_all_time.txt") as file:
                for k in file:
                    dct[kk1] = k
    with open("crypto_all_time.txt") as file:
        with open("card_all_time.txt") as f:
            for k in file:
                for j in f:
                    if int(k) > int(j):
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
            msg += f" Более выбираемая платежная система - {dict.get('best')} \n"

    msg += f"Заработано за все время - {float(dict.get('cash')) / 90}$ \n"

    msg += f"Количество регистраций за все время - {dict.get('reg')} \n"



    return msg

print(check_stat_all_time())

