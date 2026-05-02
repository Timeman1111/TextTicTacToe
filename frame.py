from term_utils import *


class Frame:
    def __init__(self):
        self.pixels: dict[tuple[int, int], tuple[int, int, int]] = {}

    def __setitem__(self, key: tuple[int, int], value: tuple[int, int, int]):
        self.pixels[key] = value

    def __getitem__(self, key: tuple[int, int]):
        return self.pixels.get(key, (0, 0, 0))

    def __iter__(self):
        return iter(self.pixels)

    def get(self, key: tuple[int, int], default: tuple[int, int, int] = (0, 0, 0)):
        return self.pixels.get(key, default)

    def __contains__(self, key: tuple[int, int]):
        return key in self.pixels

    def __repr__(self):
        return str(self.pixels)

    def __len__(self):
        return len(self.pixels)

    def compare(self, other: "Frame"):
        """
        Compares the current frame with another frame and creates a new frame containing
        the differences. The returned frame will have only the pixels that are different
        in the current frame compared to the provided `other` frame.
        """
        frame = Frame()
        # Pixels in self that are different from other
        for key, value in self.pixels.items():
            if key not in other.pixels or other.pixels[key] != value:
                frame[key] = value

        # Also need to consider pixels that were in other but are NOT in self anymore (set to 0,0,0)
        for key in other.pixels:
            if key not in self.pixels:
                frame[key] = (0, 0, 0)

        return frame




