
from functools import lru_cache

TOP_HALF_BLOCK = "▀"

def clear():
    print("\033[2J", end="")

def hide_cursor():
    print("\033[?25l", end="")

def show_cursor():
    print("\033[?25h", end="")


def generate_move_string(x: int, y: int):
    return f"\033[{y + 1};{x + 1}H"

@lru_cache(maxsize=4096)
def generate_fore_color(color: tuple[int, int, int]):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"
@lru_cache(maxsize=4096)
def generate_back_color(color: tuple[int, int, int]):
    return f"\033[48;2;{color[0]};{color[1]};{color[2]}m"

def build_pixel(top_color: tuple[int, int, int] = (0, 0, 0), bottom_color: tuple[int, int, int] = (0, 0, 0)):
    tp = generate_fore_color(top_color)
    bt = generate_back_color(bottom_color)

    px = tp + bt + TOP_HALF_BLOCK + "\033[0m"
    return px

