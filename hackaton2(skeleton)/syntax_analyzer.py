#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль призначено для перевірки синтаксичної правильності виразу та присвоєння.

Вираз може мати вигляд:
(abc + 123.5)*d2-3/(x+y)
Вираз може містити:
    змінні - ідентифікатори
    константи - дійсні або цілі числа без знаку
    знаки операцій: +, -, *, /
    дужки: (, )

Присвоєння - це

<змінна> = <вираз>
наприклад
 x = a + b

Функція check_expression_syntax за заданим списком токенів
для виразу має повернути
булівське значення та (можливо) помилку
Кожний токен - це кортеж: (<тип токену>, <значення токену>)
Перевірка робиться на допустимість сусідніх токенів,
правильний перший та останній токен, порожній вираз,
правильність розставлення дужок

Функція check_assignment_syntax за заданим списком токенів
для присвоєння має повернути
булівське значення та (можливо) помилку.
"""
from tokenizer import Token, get_tokens

# словник множин допустимих наступних токеныв для заданого токена
VALID_PAIRS = {"variable": {"operation", "right_paren"},
               "constant": {"operation", "right_paren"},
               "operation": {"variable", "constant", "left_paren"},
               "left_paren": {"left_paren", "variable", "constant"},
               "right_paren": {"right_paren", "operation"},
               "other": set()}

# словник помилок
ERRORS = {"invalid_pair": "Недопустима пара токенів {}, {}",
          "incorrect_parens": "Неправильно розставлені дужки",
          "empty_expr": "Порожній вираз",
          "incorrect_assignment": "Неправильне присвоєння",
          "invalid_start": 'Недопустимий початок або кінець'}

# кортеж допустимих перших токенів
VALID_START = ('variable', 'constant', 'left_paren')

# кортеж допустимих останніх токенів
VALID_END = ('variable', 'constant', 'right_paren')


def check_assignment_syntax(tokens):
    """
    Функція перевіряє синтаксичну правильність присвоєння за списком токенів.
    Повертає булівське значення та рядок помилки.
    Якщо помилки немає, то повертає порожній рядок.
    Використовує функцію check_expression_syntax
    :param tokens: список токенів
    :return: success - булівське значення
    :return: error - рядок помилки
    """
    succ4 = False
    errorr = ''
    error = ''
    succ1 = len(tokens) >= 2
    succ2 = False
    succ3 = False
    if succ1:
        succ2 = tokens[0].type == 'variable'
        succ3 = tokens[1].value == '='
    else:
        error = ERRORS["empty_expr"]


    if succ1 and succ2 and succ3:
        tmp_tokens = tokens[2:]

        succ4, errorr = check_expression_syntax(tmp_tokens)

    if not(succ1 and succ3 and succ2):
        error = ERRORS["incorrect_assignment"]
    elif not succ4:
        error = errorr

    return succ1 and succ3 and succ4 and succ2, error


def check_expression_syntax(tokens):
    """
    Функція перевіряє синтаксичну правильність виразу за списком токенів.
    Повертає булівське значення та рядок помилки.
    Якщо помилки немає, то повертає порожній рядок
    :param tokens: список токенів
    :return: success - булівське значення
    :return: error - рядок помилки
    """
    succ1 = True
    error = ''
    for i in range(len(tokens) - 1):
        tmp_succ = _check_pair(tokens[i], tokens[i + 1])
        if not tmp_succ:
            succ1 = False
            error = ERRORS['invalid_pair'].format(tokens[i], tokens[i + 1])
            break
    succ2 = False
    succ3 = len(tokens) != 0

    if succ3:
        succ2 = _check_start_end(tokens)
        if not succ2 and succ1:
            error = ERRORS['invalid_start']
    else:
        error = ERRORS['empty_expr']
    succ4 = _check_parens(tokens)
    if not succ4:
        error = ERRORS['incorrect_parens']

    return succ1 and succ2 and succ3 and succ4, error


def _check_parens(tokens):
    """
    Функція перевіряє чи правильно розставлені дужки у виразі.
    Повертає булівське значення
    :param tokens: список токенів
    :return: success - булівське значення
    """

    parents = 0
    succ = True
    for token in tokens:
        if token.type == 'left_paren':
            parents += 1
        elif token.type == 'right_paren':
            parents -= 1

        if parents < 0:
            succ = False
            break
    if parents != 0:
        succ = False
    return succ


def _check_pair(tok, next_tok):
    """
    Функція перевіряє чи правильна пара токенів.
    Повертає булівське значення
    :param tok: поточний токен
    :param next_tok: наступний токен
    :return: success - булівське значення
    """

    succ = next_tok.type in VALID_PAIRS[tok.type]
    return succ


def _check_start_end(tokens):

    start = tokens[0].type in VALID_START
    end = tokens[-1].type in VALID_END

    return start and end


if __name__ == "__main__":
    success1, error1 = check_expression_syntax(get_tokens("(((ab1_ - 345.56)(*/.2{_cde23"))
    success2, error2 = check_expression_syntax(get_tokens("(ab1_ - 345.56)*/.2_cde23"))
    success3, error3 = check_expression_syntax(get_tokens(" - 345.56*/.2_cde23"))
    success4, error4 = check_expression_syntax(get_tokens("2 - 345.56 *"))
    success5, error5 = check_expression_syntax(get_tokens("2 - .2"))
    success6, error6 = check_expression_syntax(get_tokens("   "))
    success7, error7 = check_expression_syntax(get_tokens("((abc -3 * b2) + d5 / 7)"))
    success8, error8 = check_assignment_syntax(get_tokens("x + y"))
    success9, error9 = check_assignment_syntax(get_tokens("x ="))
    success10, error10 = check_assignment_syntax(get_tokens("x = (a+b)"))

    success = (
        not success1 and error1 == 'Неправильно розставлені дужки' and
        not success2 and error2 ==
        "Недопустима пара токенів Token(type='operation', value='*'),"
        " Token(type='operation', value='/')" and
        not success3 and not success4 and
        not success5 and error5 ==
        "Недопустима пара токенів Token(type='operation', value='-'), "
        "Token(type='other', value='.')" and
        not success6 and error6 == "Порожній вираз" and
        success7 and error7 == "" and
        not success8 and error8 == "Неправильне присвоєння" and
        not success9 and error9 == "Порожній вираз" and
        success10 and error10 == ""
    )

    print("Success =", success)
