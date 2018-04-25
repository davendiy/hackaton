#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Виконувальний файл.

Реалізує консольний режим для інтерпретатора (запущений основний цикл, який очікує
команд від користувача)

Працює, якщо запускати пакет, як скрипт
        (через консоль: python3 -m skeleton
                -m - параметр, який вказує, що пакет запускається в режимі скрипта)

Якщо запускати сам файл, то нічого не буде, оскільки порушиться система відносного імпорта.
"""

from .code_generator import generate_code
from .interpreter import execute, ERRORS, show_variables
from .storage import clear


def print_program(program_lines):
    """
    Функція показує програму за списком її рядків
    :param program_lines: список рядків програми
    :return: None
    """
    for line in program_lines:
        print(line)


def execute_program(program_lines):
    """
    Функція виконує програму та показує стан пам'яті після виконання
    :param program_lines: список рядків програми
    :return: None
    """
    print_program(program_lines)

    # параметр clear_storage вказує на те, щоб пам'ять не очищалась,
    # як це робиться в режимі запуску скрипта
    code, error = generate_code(program_lines, clear_storage=False)
    if error:
        print("Помилка при генерації коду: {}".format(error))
        return error

    last_error = execute(code)
    if last_error:
        error = ERRORS[last_error]
        print("Помилка виконання програми: {}".format(error))
        return error

    print("Стан пам'яті")
    show_variables()
    return ""


# основний цикл
while True:
    tmp_line = [input('--> ')]
    if 'exit' == tmp_line[0].strip():
        break
    elif 'clear' == tmp_line[0].strip():
        clear()
        continue
    execute_program(tmp_line)
