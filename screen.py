"""Screen: terminal display manager with frame buffering and pixel-level rendering."""
import os
import random
import sys
from collections import deque

import numpy as np
import cv2

from frame import Frame
from term_utils import (
    init_terminal,
    clear,
    hide_cursor,
    show_cursor,
    generate_move_string,
    build_pixel,
)


class Screen:
    """
    Manages the terminal display, including cursor control and frame refreshing.
    """

    def __init__(self, last_pos: tuple[int, int] = (0, 0)):
        """
        Initializes the Screen.
        :param last_pos: Initial cursor position (y, x).
        """
        init_terminal()
        self.last_pos = last_pos
        self.width, self.height = os.get_terminal_size()

        self.p1: Frame = Frame(self.width, self.height * 2)
        self.f1: Frame = Frame(self.width, self.height * 2)

        self.is_cursor_visible = True

    def hide_cursor(self):
        """
        Hides the terminal cursor.
        """
        hide_cursor()
        self.is_cursor_visible = False

    def show_cursor(self):
        """
        Shows the terminal cursor.
        """
        show_cursor()
        self.is_cursor_visible = True

    def home_cursor(self):
        """
        Moves the terminal cursor to the top-left corner (0, 0).
        """
        self.move_cursor(0, 0)

    def move_cursor(self, x: int, vy: int):
        """
        Moves the terminal cursor to the specified position.
        :param x: X-coordinate.
        :param vy: Y-coordinate.
        """
        move_str = generate_move_string(x, vy)
        self.last_pos = (vy, x)
        self.__out(move_str, end="")

    def __getitem__(self, key: tuple[int, int]):
        """
        Gets the pixel color from the current frame.
        :param key: A tuple of (x, y) coordinates.
        :return: A tuple of (R, G, B) color values.
        """
        return self.f1[key]

    def get(self, key: tuple[int, int], default: tuple[int, int, int] = (0, 0, 0)):
        """
        Gets the pixel color from the current frame with a default value.
        :param key: A tuple of (x, y) coordinates.
        :param default: Default color to return if the pixel is not set.
        :return: A tuple of (R, G, B) color values.
        """
        return self.f1.get(key, default)

    # noinspection PyShadowingNames
    def __setitem__(self, key: tuple[int, int], value: tuple[int, int, int]):
        """
        Sets the pixel color in the current frame.
        :param key: A tuple of (x, y) coordinates.
        :param value: A tuple of (R, G, B) color values.
        """
        self.f1[key] = value

    def __out(self, text: str, end: str = "\n"):
        """
        Writes text to stdout and flushes.
        :param text: The text to write.
        :param end: The string to append at the end (default is newline).
        """
        sys.stdout.write(text + end)
        sys.stdout.flush()

    def refresh(self):
        """
        Refreshes the terminal screen by comparing the current frame with the previous one
        and outputting only the changes, or a full refresh if too many changes occur.
        """
        self.hide_cursor()

        changes = self.f1.compare(self.p1)

        if len(changes) > (self.width * self.height) // 2:
            # Full refresh
            self.home_cursor()
            output = [
                build_pixel(
                    self.f1.pixels[vy * 2 * self.width + x],
                    self.f1.pixels[(vy * 2 + 1) * self.width + x],
                )
                if x < self.width - 1
                else build_pixel(
                    self.f1.pixels[vy * 2 * self.width + x],
                    self.f1.pixels[(vy * 2 + 1) * self.width + x],
                ) + "\n"
                for vy in range(self.height)
                for x in range(self.width)
            ]
            self.__out("".join(output) + "\033[0m", end="")
        else:
            # Partial refresh
            output = []
            for (x, vy), (top, bottom) in changes.items():
                output.append(generate_move_string(x, vy) + build_pixel(top, bottom))
            self.__out("".join(output) + "\033[0m", end="")

        self.p1 = self.f1
        self.f1 = Frame(self.width, self.height * 2)

        self.move_to_bottom()

        if self.is_cursor_visible:
            self.show_cursor()

    def move_to_bottom(self):
        """
        Moves the terminal cursor to the bottom of the screen.
        """
        move_str = generate_move_string(0, self.height - 1)
        self.__out(move_str, end="")

    def draw_line(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        x: int,
        y: int,
        x2: int,
        y2: int,
        color: tuple[int, int, int],
    ):
        """
        Draws a line on the current frame using Bresenham's line algorithm.
        :param x: Starting X-coordinate.
        :param y: Starting Y-coordinate.
        :param x2: Ending X-coordinate.
        :param y2: Ending Y-coordinate.
        :param color: A tuple of (R, G, B) color values.
        """
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


class Box:
    """
    A simple rectangular box that can move and bounce off the screen boundaries.
    """

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: tuple[int, int, int],
    ):
        """
        Initializes a Box.
        :param x: Initial X-coordinate.
        :param y: Initial Y-coordinate.
        :param width: Width of the box.
        :param height: Height of the box.
        :param color: A tuple of (R, G, B) color values.
        """
        self.x = x
        self.y = y

        self.x_vel = 0
        self.y_vel = 0

        self.width = width
        self.height = height
        self.color = color

    def draw(self, t_screen: Screen):
        """
        Updates the box position and draws it on the provided screen.
        :param t_screen: The Screen object to draw on.
        """

        self.update(t_screen.width, t_screen.height * 2)

        for y in range(self.y, self.y + self.height):
            for x in range(self.x, self.x + self.width):
                t_screen[(x, y)] = self.color

    def update(self, width: int, height: int):
        """
        Updates the box position and handles bouncing off boundaries.
        :param width: The width of the boundary.
        :param height: The height of the boundary.
        """

        if self.x < 0 or self.x + self.width > width:
            self.x_vel = -self.x_vel
        if self.y < 0 or self.y + self.height > height:
            self.y_vel = -self.y_vel

        if self.x_vel == 0 and self.y_vel == 0:
            self.x_vel = random.choice((-1, 1))
            self.y_vel = random.choice((-1, 1))

        self.x += self.x_vel
        self.y += self.y_vel


class ImageSurface:
    """
    A surface that can display an image from a numpy array.
    """

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        image_array: np.ndarray,
    ):
        """
        Initializes an ImageSurface.
        :param x: Initial X-coordinate.
        :param y: Initial Y-coordinate.
        :param width: Target width of the image.
        :param height: Target height of the image.
        :param image_array: A numpy array representing the image (H, W, 3).
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Efficiently resize the image to the target dimensions using nearest neighbor interpolation
        h, w = image_array.shape[:2]
        if h != height or w != width:
            # Generate indices for interpolation
            y_indices = (np.arange(height) * (h / height)).astype(int)
            x_indices = (np.arange(width) * (w / width)).astype(int)
            # Clip indices to ensure they are within bounds
            y_indices = np.clip(y_indices, 0, h - 1)
            x_indices = np.clip(x_indices, 0, w - 1)
            scaled_array = image_array[y_indices[:, None], x_indices]
        else:
            scaled_array = image_array

        # Pre-convert to a flat list of tuples for maximum drawing efficiency
        # This allows using list slicing during the draw call
        self.pixels = [
            tuple(scaled_array[py, px])
            for py in range(height)
            for px in range(width)
        ]

    def draw(self, t_screen: Screen):  # pylint: disable=too-many-locals
        """
        Draws the image on the provided screen as efficiently as possible.
        :param t_screen: The Screen object to draw on.
        """
        f1 = t_screen.f1
        if not f1.is_flat:
            # Fallback for sparse frames
            for i in range(self.height):
                sy = self.y + i
                if 0 <= sy < t_screen.height * 2:
                    for j in range(self.width):
                        sx = self.x + j
                        if 0 <= sx < t_screen.width:
                            t_screen[(sx, sy)] = self.pixels[i * self.width + j]
            return

        # Direct access to the flat pixel list for speed
        sw = f1.width
        sh = f1.height
        target_pixels = f1.pixels

        # Calculate overlap bounds
        start_y = max(0, self.y)
        end_y = min(sh, self.y + self.height)
        start_x = max(0, self.x)
        end_x = min(sw, self.x + self.width)

        if start_y >= end_y or start_x >= end_x:
            return

        # Copy rows using list slicing
        copy_width = end_x - start_x
        img_x_offset = start_x - self.x

        for i in range(start_y, end_y):
            target_offset = i * sw + start_x
            img_y = i - self.y
            img_offset = img_y * self.width + img_x_offset

            target_pixels[target_offset: target_offset + copy_width] = (
                self.pixels[img_offset: img_offset + copy_width]
            )

    def move(self, x_pos: int, y_pos: int):
        """Shift the surface's position by (x_pos, y_pos)."""
        self.x += x_pos
        self.y += y_pos


class Video:
    """
    Manages a queue of image frames and renders them sequentially using ImageSurface.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initializes the Video object.
        :param x: Initial X-coordinate.
        :param y: Initial Y-coordinate.
        :param width: Target width for all frames.
        :param height: Target height for all frames.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.queue = deque()
        self.cursor = 0

    def input(self, img: np.ndarray):
        """
        Adds a new frame to the video queue.
        :param img: A numpy array representing the image frame.
        """
        # Pre-process the image into an ImageSurface for efficient rendering.
        # This handles resizing once upon input.
        surface = ImageSurface(self.x, self.y, self.width, self.height, img)
        self.queue.append(surface)

    def draw(self, t_screen: Screen):
        """
        Renders the next frame from the queue and advances the cursor.
        :param t_screen: The Screen object to draw on.
        """
        if not self.queue:
            return

        # Get the next frame (FIFO)
        surface = self.queue.popleft()

        # Ensure it's drawn at the Video's current coordinates
        surface.x = self.x
        surface.y = self.y

        surface.draw(t_screen)
        self.cursor += 1

    def reset(self):
        """
        Resets the frame cursor.
        """
        self.cursor = 0


def load_img(img_path: str):
    """Load an image from disk and return it as an RGB numpy array."""
    img_arr = cv2.imread(img_path)  # pylint: disable=no-member
    img_rgb_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)  # pylint: disable=no-member
    return img_rgb_arr


if __name__ == "__main__":
    clear()
    screen = Screen()
    loaded_img = load_img("test_files/test.jpg")

    IMG_SIZE = 25

    image_surface = ImageSurface(0, 0, IMG_SIZE, IMG_SIZE, loaded_img)

    try:
        while True:
            image_surface.move(1, 0)
            image_surface.draw(screen)
            screen.refresh()
            screen.move_to_bottom()

            if image_surface.x > screen.width:
                image_surface.x = 0
                image_surface.y += IMG_SIZE

            if image_surface.y + IMG_SIZE > screen.height * 2:
                image_surface.y = 0
                image_surface.x += IMG_SIZE
    except KeyboardInterrupt:
        screen.move_to_bottom()
