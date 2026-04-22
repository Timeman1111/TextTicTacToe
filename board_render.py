from board import TicTacToe


def generate_move_string(move: tuple[int, int]):
    return f"\033[{move[1]};{move[0]}H"

def generate_color_string(color: tuple[int, int, int]):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

def generate_pixel(x: int, y: int, color: tuple[int, int, int] = (255, 255, 255)):

    color_str = generate_color_string(color)
    move_str = generate_move_string((x, y))

    return f"{move_str}{color_str}█\033[0m"


class BoardRenderer:
    def __init__(self, scale: int =1):
        self.scale = scale
        self.pixel_str = "█"

        self.background_color = (255, 255, 255)
        self.border_color = (0, 0, 0)

        self.square_size = 10

    def render_board(self, x: int, y: int, board: TicTacToe):
        """
        Renders the game board of a Tic Tac Toe game by generating and displaying
        borders.

        :param x: X-coordinate to be used for border rendering.
        :param y: Y-coordinate to be used for border rendering.
        :param board: Instance of the TicTacToe class representing the game state.
        :return: None
        """
        boarders = self.generate_borders(x=x, y=y, board_size=len(board.board))

        for boarder in boarders:
            print(boarder)

    def generate_borders(self, x: int, y: int, board_size: int = 3):
        """
        Generates a list of horizontal borders for a game board based on the provided
        parameters. The function calculates the position and dimensions of each border
        based on the given starting point, board size, and square size.

        :param x: The X-coordinate of the top-left corner of the game board.
        :type x: int
        :param y: The Y-coordinate of the top-left corner of the game board.
        :type y: int
        :param board_size: The number of squares along one side of the board.
                           Defaults to 3.
        :type board_size: int
        :return: A list of generated horizontal borders for the game board.
        :rtype: list
        """
        boarders = []
        for y_step in range(board_size):
            hz = self.generate_horizontal_line(x=x, y=y + round(y_step * self.square_size / 2), width=(self.square_size * board_size) + board_size)
            boarders.append(hz)

        return boarders

    def generate_horizontal_line(self, x: int, y: int, width: int):
        """
        Generates a horizontal line by creating a series of pixels along a specified width.

        This method uses the specified starting point (`x`, `y`), the given line width, and
        the current border color of the object to generate a horizontal line represented
        as a string. Each pixel in the line is created by incrementally adjusting the x-coordinate
        while keeping the y-coordinate constant.

        This function only deals with horizontal lines, and its behavior depends on the
        `generate_pixel` function that is called for each pixel in the line.

        :param x: The x-coordinate of the starting point of the horizontal line.
        :param y: The y-coordinate of the starting point of the horizontal line.
        :param width: The total width of the horizontal line.
        :return: A string representation of the generated horizontal line.
        """
        horizontal_line = ""

        for i in range(width):
            horizontal_line += generate_pixel(x=x + i, y=y, color=self.border_color)
        return horizontal_line

