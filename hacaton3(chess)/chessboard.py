import turtle


FIGURE_CODES = {('king', 'b'): 9818,
                ('queen', 'b'): 9819,
                ('bishop', 'b'): 9821,
                ('rook', 'b'): 9820,
                ('knight', 'b'): 9822,
                ('pawn', 'b'): 9823,
                ('king', 'w'): 9812,
                ('queen', 'w'): 9813,
                ('bishop', 'w'): 9815,
                ('rook', 'w'): 9814,
                ('knight', 'w'): 9816,
                ('pawn', 'w'): 9817,
                }


class ErrorNoKing(Exception):
    def __str__(self):
        return "No king"


class ErrorEmptyCell(Exception):
    def __str__(self):
        return "Nothing to move, cell is empty"


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


class Chessboard:
    def __init__(self):
        self.t = turtle.Turtle()

    def _rev_color(self, color):
        """
        Обращает цвет черной клетки на белую, и наоборот

        :param color:
        :return:
        """
        return 'dark grey' if color == 'light grey' else 'light grey'

    def show_position(self, position):
        """
        Отрисовывает текущее состояние доски

        Отрисовка включает в себя и отрисовку доски, поэтому переставляя фигуры
        (изменяя position) желательно пользоваться следующей функцией
        а - масштаб
        :param position: <class 'Position'> instance
        :return: None
        """
        self.t.penup()
        a = 90
        # для отрисовки доски
        start_pos_x = -4 * a
        start_pos_y = 4 * a
        # для отрисовки фигур
        another_start_pos_x = -4 * a
        another_start_pos_y = -4 * a
        # цвет первой клетки
        fill_color = 'light grey'
        self.t.color()
        # цикл отрисовки всех строк
        for j in range(8):
            self.t.setpos(start_pos_x, start_pos_y)
            self.t.pendown()
            # цикл отрисовки строки
            for i in range(8):
                self.t.setpos(start_pos_x, start_pos_y)
                self.t.color('black', fill_color)
                self.t.begin_fill()
                self.t.seth(0)
                # цикл отрисовки отдельной клетки
                for k in range(4):
                    self.t.fd(a)
                    self.t.right(90)
                self.t.end_fill()
                start_pos_x += a
                fill_color = self._rev_color(fill_color)
            self.t.penup()
            fill_color = self._rev_color(fill_color)
            start_pos_x = -4 * a
            start_pos_y -= a
        figs = position.get_pos()
        # отрисовка всех фигур, используя базу всех кодов
        for pos, fig in figs.items():
            fig = (fig.get_type(), fig.get_color())
            fig_code = FIGURE_CODES[fig]
            pos_x = another_start_pos_x + pos[0] * a + int(a * 0.1)
            pos_y = another_start_pos_y + pos[1] * a + int(a * 0.05)
            self.t.up()
            self.t.setpos(pos_x, pos_y)
            # отрисовка конкретной фигуры
            self.t.write(chr(fig_code), font=('', int(a * 2 / 3)))

    def show_move(self, position, cell1, cell2):
        """
        Отрисовывает передвижение фигуры

        а - масштаб
        :param position: <class 'Position'> instance
        :param cell1: start position
        :param cell2: end position
        :return: None
        """
        cell1, cell2 = ch2py(cell1), ch2py(cell2)
        # определение цвета начальной и конечной клетки
        start_flag, end_flag = (cell1[0] + cell1[1]) % 2, (cell2[0] + cell2[1]) % 2
        start_color = 'dark grey' if start_flag == 0 else 'light grey'
        end_color = 'dark grey' if end_flag == 0 else 'light grey'
        a = 90
        start_pos_x = -4 * a
        start_pos_y = -4 * a
        figs = position.get_pos()
        try:
            figure = figs[cell1]
        except KeyError:
            raise ErrorEmptyCell
        figure = (figure.get_type(), figure.get_color())
        fig_code = FIGURE_CODES[figure]
        # --------- удаление первой фигуры с доски --------
        pos_x = start_pos_x + cell1[0] * a
        pos_y = start_pos_y + cell1[1] * a
        self.t.seth(0)
        self.t.up()
        self.t.setpos(pos_x, pos_y + a)
        self.t.color('black', start_color)
        self.t.begin_fill()
        self.t.seth(0)
        self.t.down()
        for k in range(4):
            self.t.fd(a)
            self.t.right(90)
        self.t.end_fill()
        # --------- удаление второй фигуры с доски (на случай если есть)--------
        pos_x = start_pos_x + cell2[0] * a
        pos_y = start_pos_y + cell2[1] * a
        self.t.seth(0)
        self.t.up()
        self.t.setpos(pos_x, pos_y + a)
        self.t.color('black', end_color)
        self.t.begin_fill()
        self.t.seth(0)
        self.t.down()
        for k in range(4):
            self.t.fd(a)
            self.t.right(90)
        self.t.end_fill()
        self.t.up()
        # --------- отрисовка фигуры на новой клетке ---------
        pos_x = start_pos_x + cell2[0] * a + int(a * 0.1)
        pos_y = start_pos_y + cell2[1] * a + int(a * 0.05)
        self.t.setpos(pos_x, pos_y)
        self.t.write(chr(fig_code), font=('', int(a * 2 / 3)))
        turtle.mainloop()