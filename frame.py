class Frame:
    def __init__(self):
        self.pixels: dict[tuple[int, int], tuple[int, int, int]] = {}

    def __setitem__(self, key: tuple[int, int], value: tuple[int, int, int]):
        self.pixels[key] = value

    def __getitem__(self, key: tuple[int, int]):
        return self.pixels[key]

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
        Compares the current Frame instance with another Frame instance, identifying the
        differences between their `pixels` attributes. The method returns a new Frame
        containing only the differing pixels.

        :param other: The `Frame` instance to compare against.
        :type other: Frame
        :return: A new `Frame` object containing the pixel differences between the
                 two Frame instances.
        :rtype: Frame
        """
        frame = Frame()
        for key, value in self.pixels.items():
            if (key not in other.pixels) or (value != other.pixels[key]):
                frame[key] = value

        return frame
