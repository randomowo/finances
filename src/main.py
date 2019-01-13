#!/usr/bin/env python3

import pickle
import datetime
import sys

TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
FILEPATH = "/tmp/finances.pkl"
EMPTY = [{}, [{}, 0.0]]

def account(name):
    return {name: [0.0, {TODAY: []}]}

def borrow(arr):
    if (len(arr) == 3):
        obj_list=load()[1]
        obj_list[0].update({arr[-2] : arr[-1]})
        obj_list[1] += float(arr[-1])
        save_object(obj_list, 1)
    else:
        print("err")

def new(arr):
    if (len(arr) == 2):
        obj_list=load()[0]
        if obj_list is None:
            obj_list = {}
        obj_list.update(account(arr[1]))
        save_object(obj_list, 0)
    else:
        print("err")


def remove(arr):
    if (len(arr) >= 2):
        obj_list = load()
        del obj_list[arr[1]]
        save(obj_list)
    else:
        print("err")


def changeto(arr):
    if (len(arr) == 3):
        name = arr[0]
        amount = arr[-1]
        obj_list = load()
        diff = obj_list[name][0] - float(amount)
        if (diff == 0):
            return
        obj_list[name][0] = float(amount)
        if obj_list[name][0] - float(amount) > 0:
            obj_list[name][1][TODAY].append(diff)
        else:
            obj_list[name][1][TODAY].append(-diff)
        save(obj_list)
    else:
        print("err")


def plus_or_minus(arr, pm):
    if (len(arr) == 3):
        name = arr[0]
        amount = arr[-1]
        if (amount == 0):
            return
        obj_list = load()
        obj_list[name][1][TODAY].append(float(amount) * pm)
        obj_list[name][0] += float(amount) * pm
        save(obj_list)
    else:
        print("err")


def to(arr):
    new_arr = arr[::2] + [arr[-1]]
    plus_or_minus(new_arr, -1)
    new_arr = arr[-2::-2] + [arr[-1]]
    plus_or_minus(new_arr, 1)


def info(list, dflag, accflag):
    if (len(list[1][0]) != 0 and dflag):
        print("duties amout: ", list[1][1])
        print("duties list:")
        for duty_name, duty_value in list[1][0].items():
            print("\t", duty_name, " : ", duty_value)
        if (dflag and not accflag):
            return

    if (len(list[0]) == 0 or not accflag):
        print("<empty>")
        return

    for acc_key, acc_value in list[0].items():
        print("Account name:", acc_key, "Money: ", acc_value[0])
        print("diffs:", end='')
        for in_key, in_value in acc_value[1].items():
            print("\t", in_key, " : ", in_value)


def help():
    print("""
        fin [command] [[other]]
            COMMANDS:
                new - create an account
                    new [name]

                remove - remove an account
                    remove [name]

                changeto - chamge money amount to [amount]
                    [name] changeto [amount]

                plus - increase on [amount]
                    [name] plus [amount]

                minus - decrease on [amount]
                    [name] minus [amount]

                to - transfer money through accounts
                   [name1] to [name2] [amount]

                finfo - display information of all account and thier differences and information of borrows
                    finfo
                
                dinfo - display information of borrows
                    dinfo

                ainfo - display information of all account and thier differences
                    ainfo

                borrow - add new information of borrow
                    borrow [name] [amount]

                clear - delete all info
                    clear
        """)


def save_object(obj, type):
    obj_list = load()
    obj_list[type] = obj
    save(obj_list)


def save(data):
    with open(FILEPATH, "wb") as output:
        pickle.dump(data, output)


def load():
    try:
        with open(FILEPATH, "rb") as input:
            obj_list = pickle.load(input)
    except BaseException:
        obj_list = EMPTY
    return obj_list


inp = sys.argv
del inp[0]
ACCOUNT_LIST = load()[0]
DUTY_LIST = load()[1]
inp_len = len(inp)


if (inp_len == 0):
    exit()

elif (inp[-inp_len] == "help"):
    help()

elif (inp[-inp_len] == "clear"):
    save(EMPTY)

elif (inp[-inp_len] == "ainfo"):
    info(load(), False, True)

elif (inp[-inp_len] == "dinfo"):
    info(load(), True, False)

elif (inp[-inp_len] == "finfo"):
    info(load(), True, True)

elif (inp[-inp_len] == "new"):
    new(inp)

elif (inp[-inp_len] == "remove"):
    remove(inp)

elif(inp_len > 2):
    if (inp[-inp_len] in ACCOUNT_LIST):
        if (inp[-inp_len + 1] == "changeto"):
            changeto(inp)

        elif (inp[-inp_len + 1] == "plus"):
            plus_or_minus(inp, 1)

        elif (inp[-inp_len + 1] == "minus"):
            plus_or_minus(inp, -1)

        elif (inp[-inp_len + 1] == "to" and inp[-inp_len + 2] in ACCOUNT_LIST):
            to(inp)

    elif (inp[-inp_len] == "borrow"):
        borrow(inp)
else:
    print("err")
