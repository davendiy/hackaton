#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль призначено для синтаксичного розбору виразу по частинах.

Вираз може мати вигляд:
(abc + 123.5)*d2-3/(x+y)
Вираз може містити:
    змінні - ідентифікатори
    константи - дійсні або цілі числа без знаку
    знаки операцій: +, -, *, /
    дужки: (, )

Функція get_tokens за заданим виразом має повертати
послідовність лексем - токенів
Кожний токен - це кортеж: (<тип токену>, <значення токену>)
"""
from collections import namedtuple

# типи токенів
TOKEN_TYPE = ("variable",
              "constant",
              "operation",
              "left_paren",
              "right_paren",
              "other")

# словник фіксованих токенів, що складаються з одного символа
TOKEN_TYPES = {"+": "operation",
               "-": "operation",
               "*": "operation",
               "/": "operation",
               "(": "left_paren",
               ")": "right_paren",
               "=": "equal"}
# тип токена
Token = namedtuple('Token', ['type', 'value'])


def get_tokens(string):
    """
    Функція за рядком повертає список токенів типу Token
    :param string: рядок
    :return: список токенів
    """
    tokens = []
    while string:
        token, string = _get_next_token(string)
        if token:
            tokens.append(token)
    return tokens


def _get_next_token(string):
    """
    Функція повертає наступний токен та залишок рядка
    :param string: рядок
    :return: next_tok - наступний токен, якщо є, або None
    :return: string - залишок рядка
    """
    string = _del_space(string)
    const, tmp_string1 = _get_constant(string)
    var, tmp_string2 = _get_variable(string)
    operator, tmp_string3 = _get_operator(string)
    other, tmp_string4 = _get_other(string)
    token = ''
    if const:
        string = tmp_string1
        token = Token('constant', const)
    elif var:
        string = tmp_string2
        token = Token('variable', var)
    elif operator:
        string = tmp_string3
        token = Token(TOKEN_TYPES[operator], operator)
    elif other:
        string = tmp_string4
        token = Token('other', other)

    return token, string


def _del_space(string):
    """
    функція видалення пробілів на початку рядку
    :param string: рядок
    :return: змінений рядок
    """
    while string and string[0] == ' ':
        string = string[1:] if len(string) > 1 else ''

    return string


def _get_operator(string):
    """
    функція за рядком повертає оператор (якщо є) та залишок рядка
    :param string: рядок
    :return: оператор (або дужка, якщо є), залишок рядка
    """
    operator = ''
    if string and string[0] in '*/-+()=':
        operator = string[0]
        string = string[1:] if len(string) > 1 else ''
    return operator, string


def _get_other(string):
    """
    функція за рядком повертає інші символи
    :param string: рядок
    :return: спец символ (якщо є), залишок рядка
    """
    other = ''
    if string and string[0] not in TOKEN_TYPES.keys() and string[0] != ' ':
        other = string[0]
        string = string[1:] if len(string) > 1 else ''
    return other, string


def _get_constant(string):
    """
    Функція за рядком повертає константу (якщо є) та залишок рядка
    :param string: рядок
    :return: константа (або порожній рядок), залишок рядка
    """
    t = False
    t2 = True
    var = ''
    i1 = 0
    for i, symbol in enumerate(string):
        if symbol.isdigit() or symbol == '.' and t:
            var += symbol
        else:
            t2 = False
            i1 = i
            break

        if i == 0:
            t = True
        if t and symbol == '.':
            t = False

    if t2:
        string = ''
    else:
        string = string[i1:]

    return var, string


def _get_variable(string):
    """
    Функція за рядком повертає змінну (якщо є) та залишок рядка
    :param string: рядок
    :return: змінна (або порожній рядок), залишок рядка
    """

    t = True
    var = ''
    i = 0
    while (var.isidentifier() or t) and i in range(len(string)):
        var += string[i]
        i += 1
        if t:
            t = False

    if not var.isidentifier():
        var = var[:-1]
        string = string[i - 1:]
    else:
        string = string[i:]
    return var, string


if __name__ == "__main__":

    success = get_tokens("(((ab1_ - 345.56)(*/.2{_cde23") == (
        [Token(type='left_paren', value='('),
         Token(type='left_paren', value='('),
         Token(type='left_paren', value='('),
         Token(type='variable', value='ab1_'),
         Token(type='operation', value='-'),
         Token(type='constant', value='345.56'),
         Token(type='right_paren', value=')'),
         Token(type='left_paren', value='('),
         Token(type='operation', value='*'),
         Token(type='operation', value='/'),
         Token(type='other', value='.'),
         Token(type='constant', value='2'),
         Token(type='other', value='{'),
         Token(type='variable', value='_cde23')])

    success = success and get_tokens("x = (a + b)") == [
        Token(type='variable', value='x'),
        Token(type='equal', value='='),
        Token(type='left_paren', value='('),
        Token(type='variable', value='a'),
        Token(type='operation', value='+'),
        Token(type='variable', value='b'),
        Token(type='right_paren', value=')')]
    print("Success =", success)
