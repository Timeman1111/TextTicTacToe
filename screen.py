import os
import time
import random
import sys
from frame import Frame

def clear():
    print("\033[2J", end="")

def hide_cursor():
    print("\033[?25l", end="")

def show_cursor():
    print("\033[?25h", end="")

def generate_move_string(x: int, y: int):
    return f"\033[{y + 1};{x + 1}H"

def generate_fore_color(color: tuple[int, int, int]):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

def generate_back_color(color: tuple[int, int, int]):
    return f"\033[48;2;{color[0]};{color[1]};{color[2]}m"

def calculate_slope(x1: int, y1: int, x2: int, y2: int):
    if x1 == x2:
        return float("inf")
    return (y2 - y1) / (x2 - x1)

TOP_HALF_BLOCK = "▀"



def build_pixel(top_color: tuple[int, int, int] = (0, 0, 0), bottom_color: tuple[int, int, int] = (0, 0, 0)):
    tp = generate_fore_color(top_color)
    bt = generate_back_color(bottom_color)

    px = tp + bt + TOP_HALF_BLOCK + "\033[0m"
    return px


class Screen:
    def __init__(self, last_pos: tuple[int, int] = (0, 0)):
        self.last_pos = last_pos
        self.f1: Frame = Frame()

        self.buffer = []

        self.height, self.width = os.get_terminal_size()

        self.is_cursor_visible = True



    def hide_cursor(self):
        hide_cursor()
        self.is_cursor_visible = False

    def show_cursor(self):
        show_cursor()
        self.is_cursor_visible = True

    def home_cursor(self):
        self.move_cursor(0, 0)

    def move_cursor(self, x: int, y: int):
        move_str = generate_move_string(x, y)
        self.last_pos = (y, x)
        self.__out(move_str, end="")

    def __getitem__(self, key: tuple[int, int]):
        return self.f1[key]

    def get(self, key: tuple[int, int], default: tuple[int, int, int] = (0, 0, 0)):
        return self.f1.get(key, default)





    def __setitem__(self, key: tuple[int, int], value: tuple[int, int, int]):
        x, y = key



        self.f1[key] = value

        vy = y // 2 # Divide by 2 to get the vertical position of the pixel


        if y % 2 == 0:
            btm = self.get((x, y + 1), (0, 0, 0))
            px = build_pixel(bottom_color=btm, top_color=self.f1[key])

        else:
            top = self.get((x, y - 1), (0, 0, 0))
            px = build_pixel(top, bottom_color=self.f1[key])

        self.move_cursor(x, vy)

        self._write_pixel_to_buffer(px)

    def _write_pixel_to_buffer(self, px: str):
        self.buffer.append(px)



    def __out(self, text: str, end: str = "\n"):
        sys.stdout.write(text + end)

    def refresh(self):

        self.hide_cursor()
        self.__out("".join(self.buffer))
        self.buffer.clear()

        if not self.is_cursor_visible:
            self.show_cursor()

    def move_to_bottom(self):
        move_str = generate_move_string(0, self.height - 2)
        self.__out(move_str, end="")


    def draw_line(self, x: int, y: int, x2: int, y2: int, color: tuple[int, int, int]):

        slope = calculate_slope(x, y, x2, y2) # Use function to calculate slope, should be able to handle divison by zero


        y_intercept = y - (slope * x)

        n = abs(x - (x2 + 1)) # +1 to include the x2 coordinate block as well

        for i in range(n):
            t_x: int = (x + i)
            t_y = round((slope * t_x) + y_intercept)
            self[(t_x, t_y)] = color









if __name__ == "__main__":
    clear()
    c = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 123, 0)]
    screen = Screen()


    for i in range(100):
        for x in range(screen.width):
            for y in range(screen.height):
                screen[(x, y)] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


        screen.refresh()


    screen.move_to_bottom()
