#!/usr/bin/env python3

import pickle
import datetime
import sys

TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
FILEPATH = "/tmp/finances.pkl"
EMPTY = [{}, [{}, 0.0]]


def account(name):
    """returns empty account with inputed name

    Arguments:
        name {str} -- name for account

    Returns:
        dict -- empty account
    """
    return {name: [0.0, {TODAY: []}]}


def borrow(arr):
    """adds new information about borrows

    Arguments:
        arr {list} -- inputed information
    """
    amount = arr[-1]
    if (len(arr) == 3 and isnum(amount)):
        obj_list = load()[1]
        if (arr[-2] not in obj_list[0]):
            obj_list[0].update({arr[-2]: float(amount)})
        else:
            obj_list[0][arr[-2]] += float(amount)
        obj_list[1] += float(arr[-1])
        save_object(obj_list, 1)
    else:
        print("err")


def new(arr):
    """create a new account

    Arguments:
        arr {list} -- inputed command
    """
    if (len(arr) == 2):
        obj_list = load()[0]
        if obj_list is None:
            obj_list = {}
        obj_list.update(account(arr[1]))
        save_object(obj_list, 0)
    else:
        print("err")


def remove(arr):
    """remove from data

    Arguments:
        arr {list} -- inputed command
    """
    obj_list = load()
    if (len(arr) == 2 and arr[1] in obj_list[0]):
        del obj_list[0][arr[1]]
        save(obj_list)
    else:
        print("err")


def changeto(arr):
    """Change saving amount on account 

    Arguments:
        arr {list} -- input commands
    """
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
    """increases or decreases saving on account

    Arguments:
        arr {list} -- inputed command
        pm {int} -- flag that says which operetion to do
    """
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
    """transfer savings between account

    Returns:
        list -- inputed commands
    """
    plus_or_minus(arr[::2] + [arr[-1]], -1)
    plus_or_minus(arr[-2::-2] + [arr[-1]], 1)


def info(list, binfo, accflag):
    """print stored information about finances

    Arguments:
        list {dict} -- stored information
        binfo {bool} -- flag that says print information only about borrows
        accflag {bool} -- flag that says print information only about account
    """
    if (len(list[1][0]) != 0 and binfo):
        print("duties amout: ", list[1][1])
        print("duties list:")
        for duty_name, duty_value in list[1][0].items():
            print("\t", duty_name, " : ", duty_value)
        if (binfo and not accflag):
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
    """chech is value is number

    Arguments:
        value {any} -- any value

    Returns:
        bool -- if value is float then True else False
    """
    try:
        float(value)
        return True
    except BaseException:
        return False


def help():
    """print information about command.
    """
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

                binfo - display information of borrows
                    binfo

                ainfo - display information of all account and thier differences
                    ainfo

                borrow - add new information of borrow
                    borrow [name] [amount]

                clear - delete all info
                    clear
        """)


def save_object(obj, type):
    """saves object into file

    Arguments:
        obj {dict} -- object to save 
        type {int} -- flag that says which data type save
    """
    obj_list = load()
    obj_list[type] = obj
    save(obj_list)


def save(data):
    """saves data in file

    Arguments:
        data {list} -- all data
    """
    with open(FILEPATH, "wb") as output:
        pickle.dump(data, output)


def load():
    """load data from file

    Returns:
        list -- data from file
    """
    try:
        with open(FILEPATH, "rb") as input:
            obj_list = pickle.load(input)
    except BaseException:
        obj_list = EMPTY
    return obj_list


command = {
    "help": lambda: help(),
    "clear": lambda: save(EMPTY),
    "ainfo": lambda: info(load(), False, True),
    "binfo": lambda: info(load(), True, False),
    "finfo": lambda: info(load(), True, True),
    "new": lambda: new(inp),
    "remove": lambda: remove(inp),
    "borrow": lambda: borrow(inp),
    "changeto": lambda: changeto(inp),
    "plus": lambda: plus_or_minus(inp, 1),
    "minus": lambda: plus_or_minus(inp, -1)
}


def main():
    """checks inputed command and then run needed function
    """
    inp = sys.argv[1::]
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


main()
