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
    amount = arr[-1]
    if (len(arr) == 3 and isnum(amount)):
        obj_list=load()[1]
        if (arr[-2] not in obj_list[0]):
            obj_list[0].update({arr[-2] : float(amount)})
        else:
            obj_list[0][arr[-2]] += float(amount)
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
    obj_list = load()
    if (len(arr) == 2 and arr[1] in obj_list[0]):
        del obj_list[0][arr[1]]
        save(obj_list)
    else:
        print("err")


def changeto(arr):
    obj_list = load()
    name = arr[0]
    amount = arr[-1]
    if (len(arr) == 3 and name in obj_list[0] and isnum(amount)):
        diff = obj_list[0][name][0] - float(amount)
        if (diff == 0):
            return
        obj_list[0][name][0] = float(amount)
        if obj_list[0][name][0] - float(amount) > 0:
            obj_list[0][name][1][TODAY].append(diff)
        else:
            obj_list[0][name][1][TODAY].append(-diff)
        save(obj_list)
    else:
        print("err")


def plus_or_minus(arr, pm):
    obj_list = load()
    name = arr[0]
    amount = arr[-1]
    if (len(arr) == 3 and name in obj_list[0] and isnum(amount)):
        if (amount == 0):
            return
        obj_list = load()
        obj_list[0][name][1][TODAY].append(float(amount) * pm)
        obj_list[0][name][0] += float(amount) * pm
        save(obj_list)
    else:
        print("err")


def to(arr):
    plus_or_minus(arr[::2] + [arr[-1]], -1)
    plus_or_minus(arr[-2::-2] + [arr[-1]], 1)


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
        print("\tdiffs:", end='')
        for in_key, in_value in acc_value[1].items():
            print("\t", in_key, " : ", in_value)

def isnum(value):
    try:
        float(value)
        return True
    except:
        return False

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

command = {
    "help" : lambda : help(),
    "clear" : lambda : save(EMPTY),
    "ainfo" : lambda : info(load(), False, True),
    "dinfo" : lambda : info(load(), True, False),
    "finfo" : lambda : info(load(), True, True),
    "new" : lambda : new(inp),
    "remove" : lambda : remove(inp),
    "borrow" : lambda : borrow(inp),
    "changeto" : lambda : changeto(inp),
    "plus" : lambda : plus_or_minus(inp, 1),
    "minus" : lambda : plus_or_minus(inp, -1)
}

inp = sys.argv[1::]
ACCOUNT_LIST = load()[0]
DUTY_LIST = load()[1]
inp_len = len(inp)


if (inp_len == 0):
    exit()

if (inp[-inp_len] in command):
    command[inp[-inp_len]]()

elif (inp_len > 2):

    if (inp[-inp_len + 1] in command):
        command[inp[-inp_len + 1]]()

else:
    print("err")
