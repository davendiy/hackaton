#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль призначено для реалізації пам'яті, що складається зі змінних.

Змінні можуть мати числові значення цілого або дійсного типу

"""

_storage = {}       # пам'ять
_last_error = 0     # код помилки останньої операції


# словник, що співствляє коди помилок до їх описи
ERRORS = {0: "",
          1: "Змінна вже є у пам'яті",
          2: "Змінна не існує",
          3: "Змінна невизначена"}


def add(variable):
    global _storage, _last_error
    """
    Функція додає змінну у память.
    Якщо така змінна вже існує, то встановлює помилку
    :param variable: змінна
    :return: None
    """
    if variable in _storage.keys():
        _last_error = 1
        return
    else:
        _storage[variable] = None
        _last_error = 0
        return


def is_in(variable):
    """
    Функція перевіряє, чи є змінна у пам'яті.
    :param variable: змінна
    :return: булівське значенна (True, якщо є)
    """
    global _storage, _last_error
    _last_error = 0

    return variable in _storage.keys()


def get(variable):
    """
    Функція повертає значення змінної.
    Якщо така змінна не існує або невизначена (==None),
    то встановлює відповідну помилку
    :param variable: змінна
    :return: значення змінної
    """
    global _storage, _last_error
    if variable not in _storage.keys():
        _last_error = 2
        return
    tmp = _storage.get(variable, 'KASJHDHASGFHKSAHFKJHSAKFHKSFKHBFKJBSAFBNSF')
    if tmp is None:
        _last_error = 3
        return
    _last_error = 0
    return _storage[variable]


def set(variable, value):
    """
    Функція встановлює значення змінної
    Якщо змінна не існує, повертає помилку
    :param variable: змінна
    :param value: нове значення
    :return: None
    """
    global _storage, _last_error
    if variable not in _storage.keys():
        _last_error = 2
        return
    _last_error = 0
    _storage[variable] = value
    return


def input_var(variable):
    """
    Функція здійснює введення з клавіатури та встановлення значення змінної
    Якщо змінна не існує, повертає помилку
    :param variable: змінна
    :return: None
    """
    global _storage, _last_error
    if variable not in _storage.keys():
        _last_error = 2
        return
    _last_error = 0
    _storage[variable] = float(input('Value of {}: '.format(variable)))
    return


def input_all():
    """
    Функція здійснює введення з клавіатури та встановлення значення
    усіх змінних з пам'яті
    :return: None
    """
    global _storage, _last_error
    _last_error = 0
    for var, val in _storage.items():
        _storage[var] = float(input('Value of ' + str(var) + ' '))


def clear():
    """
    Функція видаляэ усы змынны з пам'яті
    :return: None
    """
    global _storage
    global _last_error
    _last_error = 0
    _storage = {}


def get_last_error():
    """
    Функція повертає код ьостанньої помилки code
    Для виведення повідомлення треба взяти
    storage.ERRORS[code]
    усіх змінних з пам'яті
    :return: код останньої помилки
    """
    global _last_error
    return _last_error


def get_all():
    global _storage
    return _storage


if __name__ == "__main__":
    add("a")
    success = get_last_error() == 0
    add("a")
    success = success and get_last_error() == 1
    c = get("a")
    success = success and c == None and get_last_error() == 3
    c = get("b")
    success = success and c == None and get_last_error() == 2
    set("a", 1)
    success = success and get_last_error() == 0
    c = get("a")
    success = success and c == 1 and get_last_error() == 0
    set("b", 2)
    success = success and get_last_error() == 2
    add("x")
    input_var("x")      # ввести значення x = 2
    success = success and get_last_error() == 0
    f = get("x")
    success = success and f == 2 and get_last_error() == 0
    clear()
    success = success and get_last_error() == 0
    add("a")
    success = success and get_last_error() == 0
    add("d")
    success = success and get_last_error() == 0
    input_all()  # ввести значення a = 3, d = 4
    success = success and get_last_error() == 0
    c = get("a")
    success = success and c == 3 and get_last_error() == 0
    f = get("d")
    success = success and f == 4 and get_last_error() == 0
    success = success and is_in("a")

    print("Success =", success)
