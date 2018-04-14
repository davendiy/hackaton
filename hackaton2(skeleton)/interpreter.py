#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль призначено для виконання коду, який згенеровано генератором коду.
Генератор коду повертає список команд.
Кожна команда - це кортеж: (<код_команди>, <операнд>)

Інтрепретатор виконує обчислення з використанням стеку.
Стек - це список, у який ми можемо додавати до кінця та брати з кінця числа.
Щоб додати число до стеку, можна використати
_stack.append(number)
Щоб взяти число зі стеку, можна використати
number = _stack.pop()
Для виконання арифметичної операції інтерпретатор бере два останніх числа зі стеку,
обчислює результат операції та додає результат до стеку.

Допустимі команди:
("LOADC", <число>) - завантажити число у стек
("LOADV", <змінна>) - завантажити значення змінної у стек (використовується storage)
("ADD", None) - обчислити суму двох верхніх елементів стеку
("SUB", None) - обчислити різницю двох верхніх елементів стеку
("MUL", None) - обчислити добуток двох верхніх елементів стеку
("DIV", None) - обчислити частку від ділення двох верхніх елементів стеку
("SET", <змінна>) - встановити значення змінної у пам'яті (storage)
"""
from .storage import (get, clear, is_in, set as storage_set,
                      get_all, get_last_error, input_var, add)


def _loadc(number):
    """
    Функція завантажує число у стек.
    Щоб додати у стек, використовує _stack.append(...)
    Побічний ефект: встановлює значення _last_error у 0
    :param number: число
    :return: None
    """
    global _stack, _last_error
    _stack.append(float(number))
    _last_error = 0


def _loadv(variable):
    """
    Функція завантажує значення змінної з пам'яті у стек.
    Якщо змінної не існує, то встановлює відповідну помилку.
    Якщо змінна не визначена, вводить значення зміної
    за допомогою storage.
    Використовує модуль storage
    Щоб додати у стек, використовує _stack.append(...)
    Побічний ефект: змінює значення _last_error
    :param variable: ім'я змінної
    :return: None
    """
    global _stack, _last_error
    if not is_in(variable):
        _last_error = 2
        return
    if is_in(variable) and get(variable) is None:
        input_var(variable)
        _stack.append(get(variable))
        return
    if get(variable) is not None:
        _stack.append(get(variable))
    _last_error = 0


def _add(_=None):
    """
    Функція бере 2 останніх елемента зі стеку,
    обчислює їх суму та додає результат у стек.
    Щоб взяти значення зі стеку, використовує _stack.pop()
    Щоб додати у стек, використовує _stack.append(...)
    Побічний ефект: встановлює значення _last_error у 0
    :param _: ігнорується
    :return: None
    """
    global _stack, _last_error
    a1 = _stack.pop()
    a2 = _stack.pop()
    _stack.append(a1 + a2)
    _last_error = 0
    return


def _sub(_=None):
    """
    Функція бере 2 останніх елемента зі стеку,
    обчислює їх різницю та додає результат у стек.
    Щоб взяти значення зі стеку, використовує _stack.pop()
    Щоб додати у стек, використовує _stack.append(...)
    Побічний ефект: встановлює значення _last_error у 0
    :param _: ігнорується
    :return: None
    """
    global _stack, _last_error
    a1 = _stack.pop()
    a2 = _stack.pop()
    _stack.append(a2 - a1)
    _last_error = 0


def _mul(_=None):
    """
    Функція бере 2 останніх елемента зі стеку,
    обчислює їх добуток та додає результат у стек.
    Щоб взяти значення зі стеку, використовує _stack.pop()
    Щоб додати у стек, використовує _stack.append(...)
    Побічний ефект: встановлює значення _last_error у 0
    :param _: ігнорується
    :return: None
    """
    global _stack, _last_error
    a1 = _stack.pop()
    a2 = _stack.pop()
    _stack.append(a1 * a2)
    _last_error = 0


def _div(_=None):
    """
    Функція бере останнй та передостанній елементи зі стеку,
    обчислює частку від ділення передостаннього елемента на останній
    та додає результат у стек.
    Якщо дільник - 0, то встановлює помилку.
    Щоб взяти значення зі стеку, використовує _stack.pop()
    Щоб додати у стек, використовує _stack.append(...)
    Побічний ефект: встановлює значення _last_error у 0
    :param _: ігнорується
    :return: None
    """
    global _stack, _last_error

    a1 = _stack.pop()
    a2 = _stack.pop()
    if a1 == 0:
        _last_error = 3
        return
    else:
        _stack.append(a2 / a1)
        _last_error = 0
        return


def _set(variable):
    """
    Функція бере останній елемент зі стеку
    та встановлює значення змінної рівним цьому елементу.
    Якщо змінної не існує, то встановлює відповідну помилку.
    Щоб взяти значення зі стеку, використовує _stack.pop()
    Побічний ефект: змінює значення _last_error
    :param variable: ім'я змінної
    :return: None
    """
    global _stack, _last_error
    value = _stack.pop()
    storage_set(variable, value)
    if get_last_error() > 0:
        _last_error = get_last_error()
    return


COMMAND_FUNCS = {"LOADC": _loadc,
                 "LOADV": _loadv,
                 "ADD": _add,
                 "SUB": _sub,
                 "MUL": _mul,
                 "DIV": _div,
                 "SET": _set
                 }

_stack = []         # стек інтерпретатора для виконання обчислень

_last_error = 0     # код помилки останньої операції

# словник, що співствляє коди помилок до їх описи
ERRORS = {0: "",
          1: "Недопустима команда",
          2: "Змінна не існує",
          3: "Ділення на 0"}


def execute(code):
    """
    Функція виконує код програми, записаний у code.
    Повертає код останньої помилки або 0, якщо помилки немає.
    Якщо є помилка, то показує її.
    Використовує словник функцій COMMAND_FUNCS
    :param code: код програми - список кортежів (<команда>, <операнд>)
    :return: код останньої помилки або 0, якщо помилки немає
    """
    global _last_error
    for command in code:
        if command[0] not in COMMAND_FUNCS.keys():
            _last_error = 1
            break
        COMMAND_FUNCS[command[0]](command[1])
        if _last_error:
            break
    return _last_error


def show_variables():
    """
    Функція показує значення усіх змінних пам'яті
    у форматі <змінна> = <значення>
    :return: None
    """
    var = get_all()
    for i, v in var.items():
        print(i, '=', v)


if __name__ == "__main__":
    code = [('LOADC', 1.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y'),
            ('LOADV', 'x'),
            ('LOADV', 'a'),
            ('MUL', None),
            ('SET', 't'),
            ('LOADC', 1.0),
            ('LOADV', 'x'),
            ('LOADV', 'y'),
            ('SUB', None),
            ('DIV', None),
            ('SET', 'z')]
    add('x')

    add('y')
    add('a')
    add('t')
    add('z')
    last_error = execute(code)

    success = last_error == 3

    code = [('XXX', 1.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y')]
    clear()
    last_error = execute(code)

    success = success and last_error == 1

    code = [('LOADC', 1.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y')]
    clear()
    last_error = execute(code)
    print(last_error)
    success = success and last_error == 2

    code = [('LOADC', 2.0),
            ('SET', 'x'),
            ('LOADC', 1.0),
            ('SET', 'y'),
            ('LOADC', 1.0),
            ('LOADV', 'x'),
            ('LOADV', 'y'),
            ('SUB', None),
            ('DIV', None),
            ('SET', 'z')]
    clear()
    add('x')
    add('y')
    add('z')
    last_error = execute(code)

    z = get('z')
    success = success and last_error == 0 and z == 1.0

    print("Success =", success)
