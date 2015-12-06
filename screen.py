"""Deals with display/output.

"""

import doctest
import textwrap


class Screen(object):
    """You draw characters to me!

    You can print preformatted text ~*fancily*~! The screen
    object has a `set()` method to set the raw preformatted
    text contents, a `wrap()` method for how to, optionally,
    wrap said text, and finally a `decorate` attribute, for
    applying a decoration to text with a function that takes
    text and returns text.

    So you can have output that's textwrapped and inside
    a nice box with a border with padding.

    Examples:
        >>> screen = Screen(border)
        >>> screen.set("A one-liner!")
        >>> screen.draw()
        ================
        | A one-liner! |
        ----------------

    """

    def __init__(self, decorate):
        """

        Args:
            decorate (func): Takes text, returns
                modified, "decorated," text.

        """

        self._text_surface = str()
        self.decorate = decorate

    # NOTE: this seems to be an intricate
    # process... we'll circle back to making
    # this actually wrap text sometime...
    @staticmethod
    def wrap(text):
        """Return the textwrapped
        version of the supplied `text`.

        Right now, arbitrarily wraps at 60
        characters. This behavior should
        be changed in the future.

        Textwrapping, ideally, will be more
        complicated than simply:

            textwrap.wrap()

        """

        #deindented_text = textwrap.dedent(text)
        #wrapped = textwrap.fill(deindented_text, 60)

        return text

    def draw(self):
        """Draw the current screen state.

        """

        wrapped = self.wrap(self._text_surface)
        decorated = self.decorate(wrapped)

        print(decorated)

    def set(self, text):
        """Change the screen state to the
        provided `text`.

        Args:
            text (str): --

        """

        self._text_surface = text


def border(text):
    """Decorate a text block with a border!

    Args:
        text (str): Add a border around this text!

    Returns:
        str: Text with a border around it!

    Example:
        >>> print(border("A one-liner!"))
        ================
        | A one-liner! |
        ----------------

    """

    border_top_character = "="
    border_bottom_character = "-"
    border_side_character = "|"
    padding = 1

    # we're building this string as a list
    new_text = []

    # first we split up the text into lines
    lines = text.split('\n')

    # second we count the width of the longest line
    max_line_width = max([len(line) for line in lines])

    # padding occurs twice on one line
    # take longest line in text, plus two instances
    # of teh padding, plus two for the border characters
    box_width = max_line_width + (padding * 2) + 2

    border_top = border_top_character * box_width
    border_bottom = border_bottom_character * box_width

    # add a border to the top...
    new_text.append(border_top)

    # now add the sides
    for line in lines:
        # first we need the border + padding + line
        # this allows us to find out how many spaces
        # we need to reach the width of the container
        unfinished_line = "%s%s%s" % (border_side_character,
                                      padding * " ",
                                      line)

        # we add as many space characters as
        # the box size minus the length of the
        # unfinished_line, of at least one space.
        #
        # Here we prepare the aforementioned padding.
        # The -1 is the trailing border character being ommitted
        spaces = max([" ", " " * ((box_width - 1) - len(unfinished_line))])

        # here we make a new string that's unfinished line
        # plus the padding and the closing border char
        finished_line = unfinished_line + spaces + border_side_character
        
        # were done! add to the new text lines
        new_text.append(finished_line)

    # add the bottom border
    new_text.append(border_bottom)

    # now join the new_text lines with \n and return
    return '\n'.join(new_text)


if __name__ == "__main__":
    doctest.testmod()
