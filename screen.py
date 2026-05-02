import os
import time

def clear():
    print("\033[2J", end="")

def generate_move_string(x: int, y: int):
    return f"\033[{y};{x}H"

def generate_fore_color(color: tuple[int, int, int]):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

def generate_back_color(color: tuple[int, int, int]):
    return f"\033[48;2;{color[0]};{color[1]};{color[2]}m"

TOP_HALF_BLOCK = "▀"

class Screen:
    def __init__(self, last_pos: tuple[int, int] = (0, 0)):
        self.last_pos = last_pos

        self.pixels: dict[tuple[int, int], tuple[int, int, int]] = {}

        self.height, self.width = os.get_terminal_size()




    def home_cursor(self):
        self.move_cursor(0, 0)

    def move_cursor(self, x: int, y: int):
        move_str = generate_move_string(x, y)
        self.last_pos = (y, x)
        print(move_str, end="")

    def build_pixel(self, top_color: tuple[int, int, int] = (0, 0, 0), bottom_color: tuple[int, int, int] = (0, 0, 0)):
        tp = generate_fore_color(top_color)
        bt = generate_back_color(bottom_color)

        px = tp + bt + TOP_HALF_BLOCK + "\033[0m"
        return px

    def __getitem__(self, key: tuple[int, int]):
        return self.pixels[key]

    def get(self, key: tuple[int, int], default: tuple[int, int, int] = (0, 0, 0)):
        return self.pixels.get(key, default)




    def __setitem__(self, key: tuple[int, int], value: tuple[int, int, int]):
        x, y = key

        if key not in self.pixels:
            self.pixels[key] = value
        else:
            self.pixels[key] = value

        vy = y // 2


        if y % 2 == 0:
            btm = self.get((x, y + 1), (0, 0, 0))
            px = self.build_pixel(bottom_color=btm, top_color=self.pixels[key])

        else:
            top = self.get((x, y - 1), (0, 0, 0))
            px = self.build_pixel(top, bottom_color=self.pixels[key])

        self.move_cursor(x, vy)

        print(px, end = "")

    def move_to_bottom(self):
        move_str = generate_move_string(0, self.height - 2)
        print(move_str, end="")

    def draw_rect(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        pass
    def draw_line(self, x: int, y: int, x2: int, y2: int, color: tuple[int, int, int]):

        slope = (y2 - y) / (x2 - x)

        start_x = x







if __name__ == "__main__":
    clear()
    screen = Screen()
    screen.draw_line(0, 0, 10, 10, (255, 0, 0))

    screen.move_to_bottom()
