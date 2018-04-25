#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль з класами для реалізації логіки гри у шахи

"""
from collections import defaultdict
FIGURE_TYPES = ['king', 'queen', 'bishop', 'rook', 'knight', 'pawn']


class ErrorNoKing(Exception):

    def __str__(self):
        return "Відсутній король"


class ErrorGetOutOfDesk(Exception):

    def __str__(self):
        return "Координати фігури не коректні"


def ch2py(pos_ch):
    """
    function that changes string 'a1' to tuple '(0,0)'
    :param pos_ch: string of coordinates
    :return: tuple of coordinates
    """
    s = 'abcdefgh'
    y = int(pos_ch[1]) - 1
    x = s.index(pos_ch[0])
    return x, y


def ch2ch(pos_py):
    """
    Function that changes tuple '(0,0)' to string 'a1'.

    :param pos_py: tuple of coordinates
    :return: string of coordinates
    """
    s = 'abcdefgh'
    x = s[pos_py[0]]
    return x + str(pos_py[1] + 1)


class Figure:
    """
    Клас шахової фігури

    основні методи:
        get_color() -> string - повертає колір фігури
        get_type() -> string тип фігури
        get_available_moves(pos, cell) -> list - список можливих ходів
        get_available_takes(pos, cell) -> list - список можливих атак

    внутрішні методи діляться на 2 частини:
        _get_<figure>(desk, pos) -> list - список можливих ходів для кожної фігури
        _get_<figure>_takes(desk, pos_ -> list - список можливих атак для кожної фігури

    """
    def __init__(self, type_f, color):
        self._type = type_f
        self._color = color

    def __str__(self):
        return "Black " + self._type if self._color == 'b' else "White " + self._type

    def __repr__(self):
        return "Black " + self._type if self._color == 'b' else "White " + self._type

    def get_type(self):
        return self._type

    def get_color(self):
        return self._color

    def is_transform(self, pos):
        return self._type == 'pawn' and self._color == 'w' and pos[1] == 6 \
            or self._type == 'pawn' and self._color == 'b' and pos[1] == 1

    def _get_king_takes(self, desk, pos):
        """
        повертає можливі взяття для короля
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves = []
        for x in range(pos[0] - 1, pos[0] + 2):
            for y in range(pos[1] - 1, pos[1] + 2):
                figure = desk.get((x, y), 'no')
                if figure != 'no' and figure.get_color() != self._color:
                    moves.append((x, y))
        return moves

    @staticmethod
    def _get_king(desk, pos):
        """
        повертає можливі ходи для короля
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves = []
        for x in range(pos[0] - 1, pos[0] + 2):
            for y in range(pos[1] - 1, pos[1] + 2):
                figure = desk.get((x, y), 'no')
                if figure == 'no' and x in range(8) and y in range(8):
                    moves.append((x, y))

        return moves

    def _get_bishop_takes(self, desk, pos):
        """
        повертає можливі взяття для офіцера
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves = []
        for t in [(-1, -1), (1, 1), (1, -1), (-1, 1)]:
            for j in range(1, 8):
                tmp = (pos[0] + t[0] * j, pos[1] + t[1] * j)
                figure = desk.get(tmp, 'no')
                if figure == 'no':
                    continue
                elif figure.get_color() == self._color:
                    break
                elif figure.get_color() != self._color:
                    moves.append(tmp)
                    break
        return moves

    @staticmethod
    def _get_bishop(desk, pos):
        """
        повертає можливі ходи для офіцера
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves = []
        for t in [(-1, -1), (1, 1), (1, -1), (-1, 1)]:
            for j in range(1, 8):
                tmp = (pos[0] + t[0] * j, pos[1] + t[1] * j)
                figure = desk.get(tmp, 'no')
                if figure == 'no' and tmp[0] in range(8) and tmp[1] in range(8):
                    moves.append(tmp)
                else:
                    break
        return moves

    def _get_rook_takes(self, desk, pos):
        """
        повертає можливі взяття для тури
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves = []
        for t in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for j in range(1, 8):
                tmp = (pos[0] + t[0] * j, pos[1] + t[1] * j)
                figure = desk.get(tmp, 'no')
                if figure == 'no':
                    continue
                elif figure.get_color() == self._color:
                    break
                elif figure.get_color() != self._color:
                    moves.append(tmp)
                    break
        return moves

    def _get_rook(self, desk, pos):
        """
        повертає можливі ходи для короля
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves = []
        for t in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for j in range(1, 8):
                tmp = (pos[0] + t[0] * j, pos[1] + t[1] * j)
                figure = desk.get(tmp, 'no')
                if figure == 'no' and tmp[0] in range(8) and tmp[1] in range(8):
                    moves.append(tmp)
                elif figure == 'no':
                    continue
                elif figure.get_color() == self._color:
                    break
                elif figure.get_color() != self._color:
                    break
                else:
                    moves.append(tmp)
        return moves

    def _get_queen_takes(self, desk, pos):
        """
        повертає можливі взяття для королеви
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves1 = self._get_bishop_takes(desk, pos)
        moves2 = self._get_rook_takes(desk, pos)
        return moves1 + moves2

    def _get_queen(self, desk, pos):
        """
        повертає можливі ходи для королеви
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves1 = self._get_bishop(desk, pos)
        moves2 = self._get_rook(desk, pos)
        return moves1 + moves2

    def _get_knight_takes(self, desk, pos):
        """
        повертає можливі взяття для коня
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves = []
        for t in [(1, 2), (2, 1), (1, -2), (2, -1), (-1, 2), (-2, 1)]:
            tmp = (pos[0] + t[0], pos[1] + t[1])
            figure = desk.get(tmp, 'no')
            if figure != 'no' and figure.get_color() != self._color:
                moves.append(tmp)
        return moves

    @staticmethod
    def _get_knight(desk, pos):
        """
        повертає можливі ходи для коня
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves = []
        for t in [(1, 2), (2, 1), (1, -2), (2, -1), (-1, 2), (-2, 1)]:
            tmp = (pos[0] + t[0], pos[1] + t[1])
            figure = desk.get(tmp, 'no')
            if figure == 'no' and tmp[0] in range(8) and tmp[1] in range(8):
                moves.append(tmp)
        return moves

    def _get_pawn(self, desk, pos):
        """
        повертає можливі ходи для пішака
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves = []
        t = 1 if self._color == 'w' else -1
        tmp1 = (pos[0], pos[1] + t)
        tmp2 = (pos[0], pos[1] + 2 * t)

        figure = desk.get(tmp1, 'no')
        if figure == 'no' and tmp1[1] in range(8) and tmp2[1] in range(8):
            moves.append(tmp1)
            figure2 = desk.get(tmp2, 'no')
            if (t and pos[1] in range(4) or not t and pos[1] in range(4, 8)) and figure2 == 'no':
                moves.append(tmp2)

        return moves

    def _get_pawn_takes(self, desk, pos):
        """
        повертає можливі взяття для пішака
        :param desk: словник {позиція: об'єкт класу Figure}
        :param pos: кортеж (х, у)
        :return: список кортежів (х, у)
        """
        moves = []
        t = 1 if self._color == 'w' else -1
        tmp1 = (pos[0] + 1, pos[1] + t)
        tmp2 = (pos[0] - 1, pos[1] + t)
        for tmp in (tmp1, tmp2):
            figure = desk.get(tmp, 'no')
            if figure != 'no' and figure.get_color() != self._color:
                moves.append(tmp)
        return moves

    def get_available_moves(self, pos, cell):
        """
        повертає можливі ходи для фігури
        :param pos: кортеж (х, у)
        :param cell: об'єкт класу Position
        :return: список кортежів (х, у)
        """
        if self._type == 'king':
            return self._get_king(cell.current_state, pos)
        elif self._type == 'queen':
            return self._get_queen(cell.current_state, pos)
        elif self._type == 'bishop':
            return self._get_bishop(cell.current_state, pos)
        elif self._type == 'pawn':
            return self._get_pawn(cell.current_state, pos)
        elif self._type == 'rook':
            return self._get_rook(cell.current_state, pos)
        elif self._type == 'knight':
            return self._get_knight(cell.current_state, pos)

    def get_available_takes(self, pos, cell):
        """
        повертає можливі взяття для фігури
        :param pos: кортеж (х, у)
        :param cell: об'єкт класу Position
        :return: список кортежів (х, у)
        """
        if self._type == 'king':
            return self._get_king_takes(cell.current_state, pos)
        elif self._type == 'queen':
            return self._get_queen_takes(cell.current_state, pos)
        elif self._type == 'bishop':
            return self._get_bishop_takes(cell.current_state, pos)
        elif self._type == 'pawn':
            return self._get_pawn_takes(cell.current_state, pos)
        elif self._type == 'rook':
            return self._get_rook_takes(cell.current_state, pos)
        elif self._type == 'knight':
            return self._get_knight_takes(cell.current_state, pos)


class Position:
    """
    Клас реалізації шахової дошки

    методи:
        add_figure(pos, figure) -> None - додає фігуру на дошку
        take_figure(pos) -> Figure - забирає фігуру з дошки
        get_figure(pos) -> Figure - повертає фігуру з дошки, але не видаляє її
        get_figure_by_color(color) -> list - список фігур певного кольору
        get_figures_by_type_color(figure_type, color) -> list - список фігур певного типу і кольору
        create_start_position() -> None - розставляє фігури стандартним чином
        is_under_attack(cell, color) -> bool - чи знаходиться поле cell під атакою
        move(pos1, pos2, transform) -> bool - реалізує хід (повертає контрольний флаг)
        _get_all_moves_color(color) -> словник - повертає всі можливі ходи для певної сторони
        check_mate(color) -> bool - перевіряє наявність мату для певної сторони
        _create_all_possible_desks(right_moves, pre_moves) -> словник - повертає всі можливі ситуації
        find_checkmates(color, deep_step)
    """
    def __init__(self, current_state=None):
        self.current_state = current_state.copy() if current_state else {}

    def add_figure(self, pos, figure):
        if pos[0] not in range(8) or pos[1] not in range(8):
            raise ErrorGetOutOfDesk
        else:
            self.current_state[pos] = figure

    def create_start_position(self):
        """
        метод, який створює стартову позицію для шахмат

        :return: None
        """
        self.current_state = {}

        # pawns
        for j in range(8):
            tmp_figure = Figure('pawn', 'w')
            self.add_figure((j, 1), tmp_figure)
            tmp_figure = Figure('pawn', 'b')
            self.add_figure((j, 6), tmp_figure)

        # white
        self.add_figure(ch2py('a1'), Figure("rook", 'w'))
        self.add_figure(ch2py('h1'), Figure('rook', 'w'))
        self.add_figure(ch2py('b1'), Figure('knight', 'w'))
        self.add_figure(ch2py('g1'), Figure('knight', 'w'))
        self.add_figure(ch2py('c1'), Figure('bishop', 'w'))
        self.add_figure(ch2py('f1'), Figure('bishop', 'w'))
        self.add_figure(ch2py('d1'), Figure('queen', 'w'))
        self.add_figure(ch2py('e1'), Figure('king', 'w'))

        # black
        self.add_figure(ch2py('a8'), Figure("rook", 'b'))
        self.add_figure(ch2py('h8'), Figure('rook', 'b'))
        self.add_figure(ch2py('b8'), Figure('knight', 'b'))
        self.add_figure(ch2py('g8'), Figure('knight', 'b'))
        self.add_figure(ch2py('c8'), Figure('bishop', 'b'))
        self.add_figure(ch2py('f8'), Figure('bishop', 'b'))
        self.add_figure(ch2py('d8'), Figure('queen', 'b'))
        self.add_figure(ch2py('e8'), Figure('king', 'b'))

    def take_figure(self, pos):
        fig = self.current_state.get(pos, -1)
        return None if fig == -1 else self.current_state.pop(pos)

    def get_figure(self, pos):
        return self.current_state.get(pos, None)

    def get_figures_by_color(self, color):
        res = {p: f for p, f in self.current_state.items() if f.get_color() == color}
        return res

    def get_figures_by_type_color(self, figure_type, color):
        res = {p: f for p, f in self.current_state.items()
               if f.get_color() == color and f.get_type() == figure_type}
        return res

    def move(self, pos1, pos2, transform2='queen'):
        """
        функція, яка реалізує хід фігури

        :param pos1: кортеж (х, у) - стартова позиція
        :param pos2: кортеж (х, у) - кінцева позиція
        :param transform2: тип фігури, в яку трансформується пішак
        :return: Король живий - True, інакше - False
        """
        figure = self.current_state.get(pos1, None)    # отримуємо фігуру, яка стоїть на pos1
        mb_king = self.current_state.get(pos2, None)    # отримуємо фігуру, яка стоїть на pos2
        if mb_king and mb_king.get_type() == 'king':     # якщо на pos2 - король, то він вмре
            return False

        if figure is not None:     # якщо ні, то перевіряємо, чи фігура, яка ходить - пішак
            if figure.is_transform(pos1):   # якщо вона на позиції, після якої може перетворитись
                self.current_state.pop(pos1)
                self.current_state[pos2] = Figure(transform2, figure.get_color())
            else:
                self.current_state[pos2] = self.current_state.pop(pos1)
        return True

    def is_under_attack(self, cell, color):
        rev_color = 'w' if color == 'b' else 'b'
        # opposite side
        side = self.get_figures_by_color(rev_color)
        moves = []
        for pos, fig in side.items():
            moves += fig.get_available_takes(pos, self)
        # if in all possible moves
        return cell in moves

    def _get_all_moves_color(self, color):
        """
        функція пошуку всіх можливих ходів для однієї сторони

        :param color: колір сторони
        :return: словник  {key=позиція фігури: value=список можливих ходів}
        """
        side = self.get_figures_by_color(color)  # словник всіх фігур даного кольору
        king_pos = None
        moves = {}
        for pos, fig in side.items():  # створюємо словник можливих ходів для всіх фігур даного кольору
            if fig.get_type() == 'king':  # додатково запам'ятовуємо позицію короля
                king_pos = pos
            moves[pos] = fig.get_available_takes(pos, self)
            moves[pos] += fig.get_available_moves(pos, self)
        if king_pos is None:
            raise ErrorNoKing
        return king_pos, moves

    def check_mate(self, color, possible_moves=False):
        """
        функція перевірки шаха і мата

        :param color: string ('w' or 'b')
        :param possible_moves: bool (флаг чи видавати допустимі ходи)
        :return: if possible_moves:
                    bool, словник  {key=позиція фігури: value=список можливих ходів},
                 else:
                    bool
        """
        checkmate = True
        king_pos, moves = self._get_all_moves_color(color)    # отримуємо позицію короля і всі можливі ходи
        right_moves = defaultdict(list)        # словник з допустимими ходами

        if king_pos and self.is_under_attack(king_pos, color):   # якщо наявний шаг
            for pos1, mb_pos in moves.items():                # проходимо по всіх можливих ходах
                for pos2 in mb_pos:
                    tmp_king_pos = king_pos                  # якщо ходить король, то додатково запам'ятовуємо
                    if pos1 == king_pos:                     # позицію короля
                        tmp_king_pos = pos2
                    tmp_desk = Position(self.current_state)   # створюємо тимчасову дошку
                    tmp_desk.move(pos1, pos2)                  # робимо хід на цій дошці
                    if not tmp_desk.is_under_attack(tmp_king_pos, color):  # якщо після ходу королю нічого не загрошує
                        checkmate = False                                    # то ігра продовжується
                        right_moves[pos1].append(pos2)                   # записуємо цей хід до словника
        elif not king_pos:
            raise ErrorNoKing   # якщо короля не існує то видає помилку
        else:
            right_moves = moves.copy()     # якщо королю нічого не загрожує, то ігра продовжується
            checkmate = False              # і всі ходи - допустимі
        return checkmate, right_moves if possible_moves else checkmate

    def _create_all_possible_desks(self, right_moves, pre_moves):
        """
        функція, яка для даної позиції створює всі можливі

        :param right_moves: словник з допустимими ходами
        :param pre_moves: кортеж з кортежів - попередні ходи
        :return: словник {key=попередні ходи: value=об'єкт Position}
        """
        all_desks = {}
        for pos1, mb_pos in right_moves.items():    # проходимо по всіх допустимих ходах
            figure = self.current_state[pos1]
            for pos2 in mb_pos:
                if not figure.is_transform(pos1):     # якщо фігура не пішак
                    tmp_desk = Position(self.current_state)      # створюємо новий об'єкт Position
                    king_alive = tmp_desk.move(pos1, pos2)       # робимо хід
                    if king_alive:                            # якщо король залишився живий
                        all_desks[(*pre_moves, (ch2ch(pos1), ch2ch(pos2)))] = tmp_desk  # додаємо цю дошку до словника
                    else:
                        return {}           # якщо короля з'їли, то дана ситуація - некоректна
                else:
                    for transform in ('queen', 'rook', 'bishop', 'knight'):  # якщо фігура - пішак, то додатково
                        tmp_desk = Position(self.current_state)          # проходимо по всіх можливих трансформаціях

                        king_alive = tmp_desk.move(pos1, pos2, transform)   # аналогічно робимо хід
                        if king_alive and tmp_desk not in all_desks.values():
                            all_desks[(*pre_moves, (ch2ch(pos1), ch2ch(pos2), transform))] = tmp_desk
                        elif not king_alive:
                            return {}        # якщо короля з'їли, то дана ситуація - некоректна

        return all_desks

    def find_checkmates(self, color, deep_step):
        """
        функція пошуку усіх можливих шах і матів у межах даної к-ті кроків

        алгоритм - пошук в ширину: для ситуації створюємо всі можливі ситуації, а потім для
        кожної з них перевіряємо шах і мат та аналогічно створюємо далі всі можливі ситуації і т.д.
        :param color: колір сторони, яка ходить першою
        :param deep_step: ціле число - глибина пошуку
        :return: словник  {key=кортеж з кортежів - послідовність ходів, які призводять до мату:
                           value=об'єкт Position}
        """
        alter_color = 'b' if color == 'w' else 'w'
        all_desks = {'': Position(self.current_state)}   # словник, який містить в собі усі ситуації одного покоління
        all_checkmates = {}
        checkmate, right_moves = self.check_mate(color, possible_moves=True)
        if not checkmate:
            for step in range(deep_step):     # якщо на першому кроці відсутній шах і мат
                tmp_all_desks = {}     # наступне покоління

                # проходимо по всіх ситуаціях step-го покоління
                for pre, tmp_desk in all_desks.items():      # кожну ситуацію перевіряємо на шах і мат
                    tmp_checkmate, tmp_right_moves = tmp_desk.check_mate(color, possible_moves=True)
                    if not tmp_checkmate and step != deep_step - 1:     # якщо все норм, то створюємо можливі ситуації
                        tmp_all_desks.update(tmp_desk._create_all_possible_desks(tmp_right_moves, pre))
                    elif not tmp_checkmate:
                        continue     # якщо вже останнє покоління, то ситуації нафіг нада
                    elif tmp_checkmate:                             # якщо шах і мат - додаємо до словника
                        all_checkmates[pre] = tmp_desk
                all_desks = tmp_all_desks      # забуваємо теперішнє покоління і переходим до наступного
                n = len(all_desks)       # <optional> - виводимо інфу про к-ть ситуацій в поколінні
                print(n)
                alter_color, color = color, alter_color   # тепер ходить інша сторона
        return all_checkmates

    def __repr__(self):
        white_side = self.get_figures_by_color('w')
        black_side = self.get_figures_by_color('b')
        white_str, black_str = '', ''
        for pos, fig in white_side.items():
            white_str += ch2ch(pos) + ':' + str(fig) + '; '
        for pos, fig in black_side.items():
            black_str += ch2ch(pos) + ':' + str(fig) + '; '
        return str(white_str + '\n' + black_str)

    def __str__(self):
        white_side = self.get_figures_by_color('w')
        black_side = self.get_figures_by_color('b')
        white_str, black_str = '', ''
        for pos, fig in white_side.items():
            white_str += ch2ch(pos) + ':' + str(fig) + '; '
        for pos, fig in black_side.items():
            black_str += ch2ch(pos) + ':' + str(fig) + '; '
        return str(white_str + '\n' + black_str)


if __name__ == "__main__":

    DESK = Position()
    DESK.add_figure(ch2py('a7'), Figure('queen', 'w'))
    DESK.add_figure(ch2py('b3'), Figure('king', 'w'))
    DESK.add_figure(ch2py('d2'), Figure('rook', 'w'))
    DESK.add_figure(ch2py('f1'), Figure('bishop', 'w'))

    DESK.add_figure(ch2py('c6'), Figure('king', 'b'))
    DESK.add_figure(ch2py('d6'), Figure('pawn', 'b'))

    input("press enter to continue")
    print("checkmate, right_moves:")
    print(DESK.check_mate('w', possible_moves=True))
    print(DESK.check_mate('b', possible_moves=True))

    input("press enter to continue")

    print('find_checkmates:')
    checkmates = DESK.find_checkmates('w', 5)
    for i in checkmates.keys():
        print(i)

    # input('press enter to continue')
    # DESK2 = Position()
    # DESK2.create_start_position()
    # checkmates = DESK2.find_checkmates('w', 5)
    # for i in checkmates.keys():
    #     print(i)
