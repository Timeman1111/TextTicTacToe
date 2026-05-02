import os
import time
import random
import sys
from frame import Frame
from term_utils import *

class Screen:
    def __init__(self, last_pos: tuple[int, int] = (0, 0)):
        self.last_pos = last_pos
        self.p1: Frame = Frame()
        self.f1: Frame = Frame()

        self.width, self.height = os.get_terminal_size()

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

    # noinspection PyShadowingNames
    def __setitem__(self, key: tuple[int, int], value: tuple[int, int, int]):
        self.f1[key] = value




    def __out(self, text: str, end: str = "\n"):
        sys.stdout.write(text + end)

    def refresh(self):
        self.hide_cursor()
        self.home_cursor()

        output = []
        for vy in range(self.height):
            for x in range(self.width):
                top_color = self.f1.get((x, vy * 2), (0, 0, 0))
                bottom_color = self.f1.get((x, vy * 2 + 1), (0, 0, 0))
                output.append(build_pixel(top_color, bottom_color))
            output.append("\n")

        self.__out("".join(output), end="")

        self.p1 = self.f1
        self.f1 = Frame()

        self.move_to_bottom()

        if self.is_cursor_visible:
            self.show_cursor()

    def move_to_bottom(self):
        move_str = generate_move_string(0, self.height - 1)
        self.__out(move_str, end="")


    def draw_line(self, x: int, y: int, x2: int, y2: int, color: tuple[int, int, int]):
        dx = abs(x2 - x)
        dy = abs(y2 - y)
        sx = 1 if x < x2 else -1
        sy = 1 if y < y2 else -1
        err = dx - dy

        while True:
            self[(x, y)] = color
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy









if __name__ == "__main__":
    clear()
    c = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 123, 0)]
    screen = Screen()

    frame_durations = []
    for i in range(100):
        st = time.perf_counter()
        for x in range(screen.width):
            for y in range(screen.height * 2):
                screen[(x, y)] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


        screen.refresh()

        et = time.perf_counter()

        frame_durations.append(et - st)


    avg_frame_duration = sum(frame_durations) / len(frame_durations)



    screen.move_to_bottom()
    print(f"Time taken: {avg_frame_duration} seconds\n\nFPS: {1 / avg_frame_duration}")