
def generate_move_string(move: tuple[int, int]):
    return f"\033[{move[1]};{move[0]}H"

def generate_color_string(color: tuple[int, int, int]):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

def generate_pixel(x: int, y: int, color: tuple[int, int, int] = (255, 255, 255)):
    color_str = generate_color_string(color)
    move_str = f"\033[{y};{x}H"
    return f"{move_str}{color_str}█\033[0m"

class Renderable:
    def render(self) -> str:
        raise NotImplementedError("Renderable must implement render()")


class VerticalLine(Renderable):
    def __init__(self, x: int, y: int, length: int, color: tuple[int, int, int] = (255, 255, 255)):
        self.x = x
        self.y = y
        self.length = length
        self.color = color

    def render(self) -> str:
        return self.__generate_vertical_line()

    def __generate_vertical_line(self):

        ls: list[str] = [generate_pixel(x=self.x, y=self.y + i, color=self.color) for i in range(self.length)]
        return "".join(ls)


class HorizontalLine(Renderable):
    def __init__(self, x: int, y: int, length: int, color: tuple[int, int, int] = (255, 255, 255)):
        self.x = x
        self.y = y
        self.length = length
        self.color = color

    def render(self) -> str:
        return self.__generate_horizontal_line()

    def __str__(self) -> str:
        return self.render()


    def __generate_horizontal_line(self) -> str:

        ls: list[str] = [generate_pixel(x=self.x + i, y=self.y, color=self.color) for i in range(self.length)]
        return "".join(ls)


