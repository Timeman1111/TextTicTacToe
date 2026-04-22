from board import TicTacToe
from board_renderables import *
import os

def move_to_bottom():
    lines, columns = os.get_terminal_size()
    move_str = generate_move_string((0, lines - 1))
    print(move_str, end="")

def clamp(min_val, value: float | int):
    return max(min_val, value)



class BoardRenderer:
    def __init__(self, scale: int =1):
        self.scale = scale
        self.pixel_str = "█"

        self.background_color = (255, 255, 255)
        self.border_color = (255, 255, 255)

        self.square_size = 11
        self.vertical_extra = round(self.square_size / 2)

        self.x_color = (255, 0, 0)
        self.y_color = (0, 255, 0)

    def render_board(self, x: int, y: int, board: TicTacToe):

        boarders: list[Renderable] = self.generate_borders(x=x, y=y, board_size=len(board.board))

        squares: list[Renderable] = self.generate_board_squares(x=x, y=y, board=board)

        self.out(squares)
        self.out(boarders)

    def move_to_bottom(self):
        move_to_bottom()

    def generate_board_squares(self, x: int, y: int, board: TicTacToe):
        square_size = self.square_size * self.scale

        squares: list[Renderable] = []

        for by in range(len(board.board)):
            for bx in range(len(board.board[y])):
                cell_value = board.board[by][bx]

                if cell_value == 0:
                    continue

                if cell_value == 1:
                    cell_x = (bx * square_size) + x
                    cell_y = (by * square_size) + y
                    xcell = XCell(x=cell_x, y=cell_y, size = square_size, color=self.x_color)
                    squares.append(xcell)

                elif cell_value == 2:
                    cell_x = (bx * square_size) + x
                    cell_y = (by * square_size) + y
                    ocell = OCell(x=cell_x, y=cell_y, size = square_size, color=self.y_color)
                    squares.append(ocell)

        return squares


    def out(self, renderables: list[Renderable]):
        for renderable in renderables:
            print(renderable.render(), end="")

    def generate_borders(self, x: int, y: int, board_size: int = 3):
        boarders: list[Renderable] = []


        lines_c = board_size + 1

        length = (self.square_size * board_size)
        vert_lines = self.__generate_vertical_lines(x=x, y=y, length=length,spacing=self.square_size, line_count=lines_c)

        hor_lines = self.__generate_horizontal_lines(x=x, y=y, length=length,spacing=self.square_size, line_count=lines_c)

        boarders.extend(vert_lines)
        boarders.extend(hor_lines)




        return boarders


    def __generate_vertical_lines(self, x: int, y: int, length: int, spacing: int, line_count: int = 4) -> list[VerticalLine]:
        lines: list[VerticalLine] = []
        for x_step in range(line_count):
            vz = VerticalLine(x=(x + (x_step * spacing) * self.scale), y=y, length=length * self.scale, color=self.border_color)
            lines.append(vz)

        return lines

    def __generate_horizontal_lines(self, x: int, y: int, spacing: int, length: int, line_count: int = 4) -> list[HorizontalLine]:
        lines: list[HorizontalLine] = []
        for y_step in range(line_count):
            hz = HorizontalLine(x=x, y=y + ((y_step * spacing) * self.scale), length=length * self.scale, color=self.border_color)
            lines.append(hz)

        return lines


