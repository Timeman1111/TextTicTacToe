
def generate_move_string(move: tuple[int, int]):
    return f"\033[{move[1]};{move[0]}H"

def generate_color_string(color: tuple[int, int, int]):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

def generate_pixel(color: tuple[int, int, int] = (255, 255, 255)):
    color_str = generate_color_string(color)
    return f"{color_str}█\033[0m"

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


        ls: list[str] = [generate_move_string((self.x, self.y + i)) + generate_pixel(color=self.color) for i in range(self.length)]
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
        move_str = generate_move_string((self.x, self.y))

        ls: list[str] = [generate_pixel(color=self.color) for i in range(self.length)]
        return move_str +  "".join(ls)


class XCell(Renderable):
    def __init__(self, x: int, y: int, size: int, color: tuple[int, int, int] = (255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color
        self.size = size


    def render(self) -> str:
        return self.__generate_x()

    def __generate_x(self):

        ls = []

        for i in range(self.size):
            up_px = generate_move_string((self.x + i, self.y + i)) + generate_pixel(color=self.color)
            down_pixel = generate_move_string((self.x + i, self.y + self.size - i - 1)) + generate_pixel(color=self.color)
            ls.append(up_px)
            ls.append(down_pixel)



        return "".join(ls)





