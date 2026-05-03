import sys
import os
from functools import lru_cache
import random
TOP_HALF_BLOCK = "▀"

def init_terminal():
    if os.name == 'nt':
        try:
            import ctypes
            from ctypes import wintypes

            kernel32 = ctypes.windll.kernel32
            # STD_OUTPUT_HANDLE = -11
            h_stdout = kernel32.GetStdHandle(-11)
            # STD_INPUT_HANDLE = -10
            h_stdin = kernel32.GetStdHandle(-10)

            # Enable ANSI support
            mode = wintypes.DWORD()
            if kernel32.GetConsoleMode(h_stdout, ctypes.byref(mode)):
                # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                kernel32.SetConsoleMode(h_stdout, mode.value | 0x0004)

            # Disable QuickEdit Mode
            if kernel32.GetConsoleMode(h_stdin, ctypes.byref(mode)):
                # ENABLE_QUICK_EDIT_MODE = 0x0040, ENABLE_EXTENDED_FLAGS = 0x0080
                new_mode = (mode.value & ~0x0040) | 0x0080
                kernel32.SetConsoleMode(h_stdin, new_mode)
        except Exception:
            pass

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

@lru_cache(maxsize=16384)
def build_pixel(top_color: tuple[int, int, int] = (0, 0, 0), bottom_color: tuple[int, int, int] = (0, 0, 0)):
    tp = f"\033[38;2;{top_color[0]};{top_color[1]};{top_color[2]}m"
    bt = f"\033[48;2;{bottom_color[0]};{bottom_color[1]};{bottom_color[2]}m"
    return tp + bt + TOP_HALF_BLOCK

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
