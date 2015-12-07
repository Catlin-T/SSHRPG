import textwrap
import colorama
import collections


class Display(object):
    """This is the console/display.

    """

    def __init__(self, whitespace=" ", effect=None):
        # NOTE: need to auto get size and update dynamically
        # for scaling purposes
        self.resolution = (60, 40)

        self.whitespace = whitespace

        # make a blank string based off resolution
        blank_line = (whitespace * self.resolution[0])  # x
        self._lines = [blank_line for i in xrange(self.resolution[1])]
        
        # effect
        # this is ran right before the screen is rendered, but
        # doesn't change lines
        self.effect = effect

    def put_inline(self, string_to_insert, put_at_x, put_at_y):
        """Put the string_to_insert at position
        (x, y)!

        If you draw something and its tail goes
        over the edge of the display, it is simply
        cut off/truncated.

        """

        selected_line = self._lines[put_at_y]
        selected_line_as_list = [character for character in selected_line]
        ending_x_coordinate = min([self.resolution[0], len(string_to_insert) + put_at_x])
        start_end_difference = ending_x_coordinate - put_at_x

        selected_line_as_list[put_at_x:ending_x_coordinate] = string_to_insert[:start_end_difference]

        self._lines[put_at_y] = ''.join(selected_line_as_list)

    def put_multiline(self, multiline_string, put_at_x, put_at_y):
        lines = multiline_string.split('\n')

        for line in lines:
            self.put_inline(line, put_at_x, put_at_y)
            put_at_y += 1

    def draw(self):
        """Draw the state!"""

        draw_these_lines = self._lines

        if self.effect:
            draw_these_lines = self.effect(self._lines)

        print("\n".join(draw_these_lines))


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


test = Display('.', effect=rainbow_lines)
test.put_inline("butt ass mode mother fucker bitch tits", 30, 10)
test.put_multiline("""Haha
Isn't this

     really

           fucking
                  coool!?!?""", 10, 20)
test.draw()
