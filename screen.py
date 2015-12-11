import textwrap
import colorama
import collections
import os
import sys


class Display(object):
    """This is the console/display.
    
    Responsibilities:
    -Final drawing to screen
    -Container for tiles
    -Has current console resolution

    Does Not (directly):
    -take any input from player
    -display text
    -apply effects

    """

    def __init__(self, whitespace=" ", effect=None):

        self.resolution = self.get_console_resolution()

        self.whitespace = whitespace

        # make a blank string based off resolution
        blank_line = (whitespace * self.resolution[0])  # x
        self._lines = [blank_line for i in xrange(self.resolution[1])]
        
        self.tiles = {}

    def get_console_resolution(self):
        """Returns the current console width and height
        as an (x, y) tuple

        NOTE: only compatible with unix-like OS's

        """

        height, width = os.popen('stty size', 'r').read().split()

        return (int(width), int(height))

    def put_inline(self, string_to_insert, put_at_x, put_at_y):
        """Put the string_to_insert at position
        (x, y)!

        If you draw something and its tail goes
        over the edge of the display, it is simply
        cut off/truncated.

        """

        selected_line = self._lines[put_at_y]
        selected_line_as_list = [character for character in selected_line]
        ending_x_coordinate = min([self.resolution[0], 
                                  len(string_to_insert) + put_at_x])
        start_end_difference = ending_x_coordinate - put_at_x

        selected_line_as_list[put_at_x:ending_x_coordinate] = string_to_insert[:start_end_difference]

        self._lines[put_at_y] = ''.join(selected_line_as_list)

    def put_multiline(self, multiline_string, put_at_x, put_at_y):
        """Puts a multiline string or list of strings into the display
        or tile

        """

        try:
            lines = multiline_string.split('\n')
        except AttributeError: #multiline_string is already a list
            lines = multiline_string

        for line in lines:
            self.put_inline(line, put_at_x, put_at_y)
            put_at_y += 1

    def draw(self):
        """Draw the state!"""

        for tile in self.tiles.values():
            self.put_multiline(tile._lines, tile.put_tile_at_xy[0],
                               tile.put_tile_at_xy[1])

        draw_these_lines = self._lines

        #if self.effect:
        #    draw_these_lines = self.effect(self._lines)

        print("\n".join(draw_these_lines))

    def create_tile(self, label, width_percentage, height_percentage,
                    x_offset, y_offset):
        """Create a tile and add it to the tiles dict."""

        self.tiles[label] = Tile(width_percentage, height_percentage,
                                 x_offset, y_offset)


class Tile(Display):
    """Tile objects will be the main objects that the users
    interact with.

    """
    def __init__(self, width_percentage, height_percentage, 
                 x_offset_percentage, y_offset_percentage, whitespace=' '):
        """

            Args:
                width_percentage (float): The amount of the total display that
                                          this tile will take up horozontally.
                                          Arg must be between 0 and 1.

                height_percentage (float): The amount of the total display that
                                           this tile will take up vertically.
                                           Arg must be between 0 and 1.

                x_offset_percentage (float): --

                y_offset_percentage (float): --

                whitespace (char): The character that makes up the background
                                   of the tile

        """

        self.width_percentage = width_percentage
        self.height_percentage = height_percentage
        self.x_offset_percentage = x_offset_percentage
        self.y_offset_percentage = y_offset_percentage
        self.whitespace = whitespace

        self.check_offset()

        self.resolution = self.get_tile_resolution()

        self.put_tile_at_xy = self.get_xy_offset()

        # make a blank string based off resolution
        blank_line = (whitespace * self.resolution[0])  # x
        self._lines = [blank_line for i in xrange(self.resolution[1])]
        
        # effect
        # this is ran right before the screen is rendered, but
        # doesn't change lines
        #self.effect = effect

    def check_offset(self):
        """Checks that the X and Y offsets don't push the tile off 
        the display.

        Since the width and height percentages are floating points
        between 0 (none existent) and 1 (taking up the whole screen).
        The amount of space we can use to offset the tile is the 
        remainder of the total space after we calculate the width/height
        percentages.

        """

        x_offset_remainder = 1.0 - self.width_percentage
        y_offset_remainder = 1.0 - self.height_percentage

        if self.x_offset_percentage > x_offset_remainder:
            raise TileOffsetError()

        if self.y_offset_percentage > y_offset_remainder:
            raise TileOffsetError()

        return None

    def get_tile_resolution(self):
        """Returns the resolution of the tile compared to the display

        """
        
        console_resolution = self.get_console_resolution()

        width = int(console_resolution[0] * self.width_percentage)
        height = int(console_resolution[1] * self.height_percentage)

        return (width, height)

    def get_xy_offset(self):
        """Returns the x and y coordinates that the tile starts at"""
        
        console_resolution = self.get_console_resolution()

        x_offset = int(console_resolution[0] * self.x_offset_percentage)
        y_offset = int(console_resolution[1] * self.y_offset_percentage)

        return (x_offset, y_offset)


class TileOffsetError(Exception):
    """Raised when a tile's offset value would make part of it
    draw off screen

    """

    def __init__(self):
        self.msg = "Ya dun fucked up with that tile right thur."


def rainbow_lines(lines):
    """Take the lines and make em a diff color per row hyuck

    """

    # we'll rotate this array and always pick the first value
    color_wheel = [colorama.Back.BLACK, colorama.Back.RED,
                   colorama.Back.GREEN, colorama.Back.YELLOW,
                   colorama.Back.BLUE, colorama.Back.MAGENTA,
                   colorama.Back.CYAN, colorama.Back.WHITE]
    color_wheel = collections.deque(color_wheel)

    new_lines = []
    x_offset = 0

    for line in lines:
        # We could do this:
        #     new_lines.append(color_wheel[0] + line + colorama.Back.RESET)
        # But this is way cooler:
        new_lines.append(line[:x_offset] + color_wheel[0] + line[x_offset:])
        color_wheel.rotate()
        x_offset += 1

    return new_lines


test = Display('.')

test.create_tile("tile1", 0.5, 0.25, 0.2, 0.3)

test.create_tile("tile2", 0.2, 0.2, 0.7, 0.7)

test.tiles["tile2"].put_inline("FUCK YES I DID IT", 3, 4)

test.tiles["tile1"].put_multiline("""Tile
    fucking

    one
            bitch-face!""", 10, 5)
#test.put_inline("butt ass mode mother fucker bitch tits", 30, 10)
#test.put_multiline("""Haha
#Isn't this
#
#     really
#
#           fucking
#                  coool!?!?""", 10, 20)
#

test.draw()
