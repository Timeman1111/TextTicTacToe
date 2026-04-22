from board import TicTacToe


def clamp(min_val, value: float | int):
    return max(min_val, value)

def generate_move_string(move: tuple[int, int]):
    return f"\033[{move[1]};{move[0]}H"

def generate_color_string(color: tuple[int, int, int]):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

def generate_pixel(x: int, y: int, color: tuple[int, int, int] = (255, 255, 255)):
    color_str = generate_color_string(color)
    move_str = f"\033[{y};{x}H"
    return f"{move_str}{color_str}█\033[0m"


class BoardRenderer:
    def __init__(self, scale: int =1):
        self.scale = scale
        self.pixel_str = "█"

        self.background_color = (255, 255, 255)
        self.border_color = (0, 0, 0)

        self.square_size = 10
        self.vertical_extra = round(self.square_size / 2)

    def render_board(self, x: int, y: int, board: TicTacToe):
        boarders = "".join(self.generate_borders(x=x, y=y, board_size=len(board.board)))
        print("".join(boarders))

    def generate_borders(self, x: int, y: int, board_size: int = 3):
        boarders: list[str] = []
        start_y = y - (self.square_size * self.scale)

        length = ((self.square_size * board_size) + board_size) * self.scale
        for x_step in range(board_size + 1):
            vz = self.generate_vertical_line(x=x + (int((self.square_size * x_step))) * self.scale, y=start_y, length=length // 2)
            boarders.append(vz)

        start_x = x - (self.square_size * self.scale)
        for y_step in range(board_size + 1):
            hz = self.generate_horizontal_line(x=start_x, y=int(start_y + (y_step * ((self.square_size / 2)) * self.scale)), length=length)
            boarders.append(hz)


        return boarders

    def generate_horizontal_line(self, x: int, y: int, length: int) -> str:
        ls: list[str] = [generate_pixel(x + i, y, self.border_color) for i in range(length)]
        return "".join(ls)


    def generate_vertical_line(self, x: int, y: int, length: int) -> str:
        x = self.vertical_extra + x
        LS = [generate_pixel(x=x, y=y + i, color=self.border_color) for i in range(length)]
        return "".join(LS)
