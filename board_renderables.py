"""Renderable objects for the TicTacToe board: lines, X cells, and O cells."""
import math


def generate_move_string(move: tuple[int, int]):
    """Return an ANSI escape string that moves the cursor to the given (col, row) position."""
    return f"\033[{move[1]};{move[0]}H"


def generate_color_string(color: tuple[int, int, int]):
    """Return an ANSI foreground color escape string for the given RGB color."""
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"


def generate_pixel(color: tuple[int, int, int] = (255, 255, 255)):
    """Return a single colored block character with ANSI color codes."""
    color_str = generate_color_string(color)
    return f"{color_str}█\033[0m"


class Renderable:  # pylint: disable=too-few-public-methods
    """Base class for objects that can render themselves as an ANSI string."""

    def render(self) -> str:
        """Return the ANSI string representation of this renderable."""
        raise NotImplementedError("Renderable must implement render()")


class VerticalLine(Renderable):  # pylint: disable=too-few-public-methods
    """A vertical line of colored block characters."""

    def __init__(self, x: int, y: int, length: int, color: tuple[int, int, int] = (255, 255, 255)):
        """Initialize the vertical line at (x, y) with the given length and color."""
        self.x = x
        self.y = y
        self.length = length
        self.color = color

    def render(self) -> str:
        """Return the ANSI string that draws this vertical line."""
        return self.__generate_vertical_line()

    def __generate_vertical_line(self):
        ls = [
            generate_move_string((self.x, self.y + i)) + generate_pixel(color=self.color)
            for i in range(self.length)
        ]
        return "".join(ls)


class HorizontalLine(Renderable):
    """A horizontal line of colored block characters."""

    def __init__(self, x: int, y: int, length: int, color: tuple[int, int, int] = (255, 255, 255)):
        """Initialize the horizontal line at (x, y) with the given length and color."""
        self.x = x
        self.y = y
        self.length = length
        self.color = color

    def render(self) -> str:
        """Return the ANSI string that draws this horizontal line."""
        return self.__generate_horizontal_line()

    def __str__(self) -> str:
        return self.render()

    def __generate_horizontal_line(self) -> str:
        move_str = generate_move_string((self.x, self.y))
        ls = [generate_pixel(color=self.color) for _ in range(self.length)]
        return move_str + "".join(ls)


class XCell(Renderable):  # pylint: disable=too-few-public-methods
    """A cell that renders an X shape using colored block characters."""

    def __init__(self, x: int, y: int, size: int, color: tuple[int, int, int] = (255, 255, 255)):
        """Initialize the XCell at (x, y) with the given size and color."""
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def render(self) -> str:
        """Return the ANSI string that draws this X cell."""
        return self.__generate_x()

    def __generate_x(self):
        ls = []
        for i in range(1, self.size):
            up_px = (
                generate_move_string((self.x + i, self.y + i))
                + generate_pixel(color=self.color)
            )
            down_pixel = (
                generate_move_string((self.x + i, self.y + self.size - i))
                + generate_pixel(color=self.color)
            )
            ls.append(up_px)
            ls.append(down_pixel)
        return "".join(ls)


class OCell(Renderable):  # pylint: disable=too-few-public-methods
    """A cell that renders an O (circle) shape using colored block characters."""

    def __init__(self, x: int, y: int, size: int, color: tuple[int, int, int] = (255, 255, 255)):
        """Initialize the OCell at (x, y) with the given size and color."""
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def render(self) -> str:
        """Return the ANSI string that draws this O cell."""
        return self.__generate_o()

    def __generate_o(self):
        radius = (self.size - 2) / 2

        center_x = self.x + (self.size / 2)
        center_y = self.y + (self.size / 2)

        ls = []
        for i in range(self.size):
            for j in range(self.size):
                curr_x = self.x + i
                curr_y = self.y + j

                dst = math.sqrt((curr_x - center_x) ** 2 + (curr_y - center_y) ** 2)
                if abs(dst - radius) < 0.5:
                    ls.append(
                        generate_move_string((curr_x, curr_y))
                        + generate_pixel(color=self.color)
                    )

        return "".join(ls)
