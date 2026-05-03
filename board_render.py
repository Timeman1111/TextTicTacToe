"""Board rendering: translates TicTacToe state into ANSI terminal output."""
import os

from board import TicTacToe
from board_renderables import (
    HorizontalLine,
    OCell,
    Renderable,
    VerticalLine,
    XCell,
    generate_move_string,
)


def move_to_bottom():
    """Move the terminal cursor to the last row."""
    lines, _ = os.get_terminal_size()
    move_str = generate_move_string((0, lines - 1))
    print(move_str, end="")


def clamp(min_val, value: float | int):
    """Return value clamped to be at least min_val."""
    return max(min_val, value)


class BoardRenderer:  # pylint: disable=too-many-instance-attributes
    """Renders a TicTacToe board as ANSI block graphics in the terminal."""

    def __init__(self, scale: int = 1):
        """Initialize the renderer with an optional pixel scale factor."""
        self.scale = scale
        self.pixel_str = "█"

        self.background_color = (255, 255, 255)
        self.border_color = (255, 255, 255)

        self.square_size = 11
        self.vertical_extra = round(self.square_size / 2)

        self.x_color = (255, 0, 0)
        self.y_color = (0, 255, 0)

    def render_board(self, x: int, y: int, board: TicTacToe):
        """Render the full board (squares and borders) at the given terminal position."""
        borders: list[Renderable] = self.generate_borders(
            x=x, y=y, board_size=len(board.board)
        )
        squares: list[Renderable] = self.generate_board_squares(x=x, y=y, board=board)

        self.out(squares)
        self.out(borders)

    def move_to_bottom(self):
        """Move the terminal cursor to the last row."""
        move_to_bottom()

    def generate_board_squares(self, x: int, y: int, board: TicTacToe):
        """Return a list of Renderable objects for each claimed cell on the board."""
        square_size = self.square_size * self.scale

        squares: list[Renderable] = []

        for by, row in enumerate(board.board):
            for bx, cell_value in enumerate(row):
                if cell_value == 0:
                    continue

                cell_x = (bx * square_size) + x
                cell_y = (by * square_size) + y

                if cell_value == 1:
                    xcell = XCell(x=cell_x, y=cell_y, size=square_size, color=self.x_color)
                    squares.append(xcell)
                elif cell_value == 2:
                    ocell = OCell(x=cell_x, y=cell_y, size=square_size, color=self.y_color)
                    squares.append(ocell)

        return squares

    def out(self, renderables: list[Renderable]):
        """Print each renderable's ANSI output to the terminal."""
        for renderable in renderables:
            print(renderable.render(), end="")

    def generate_borders(self, x: int, y: int, board_size: int = 3):
        """Return a list of Renderable border lines for a board of the given size."""
        borders: list[Renderable] = []

        lines_c = board_size + 1

        length = self.square_size * board_size
        vert_lines = self.__generate_vertical_lines(
            x=x, y=y, length=length, spacing=self.square_size, line_count=lines_c
        )
        hor_lines = self.__generate_horizontal_lines(
            x=x, y=y, length=length, spacing=self.square_size, line_count=lines_c
        )

        borders.extend(vert_lines)
        borders.extend(hor_lines)

        return borders

    def __generate_vertical_lines(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        x: int,
        y: int,
        length: int,
        spacing: int,
        line_count: int = 4,
    ) -> list[VerticalLine]:
        """Generate vertical border lines."""
        lines: list[VerticalLine] = []
        for x_step in range(line_count):
            vz = VerticalLine(
                x=(x + (x_step * spacing) * self.scale),
                y=y,
                length=length * self.scale,
                color=self.border_color,
            )
            lines.append(vz)
        return lines

    def __generate_horizontal_lines(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        x: int,
        y: int,
        spacing: int,
        length: int,
        line_count: int = 4,
    ) -> list[HorizontalLine]:
        """Generate horizontal border lines."""
        lines: list[HorizontalLine] = []
        for y_step in range(line_count):
            hz = HorizontalLine(
                x=x,
                y=y + ((y_step * spacing) * self.scale),
                length=length * self.scale,
                color=self.border_color,
            )
            lines.append(hz)
        return lines
