"""Segment.

Handles storage and rendering of ANSI-decorated single characters.
"""


class Segment:
    """Segment.

    Handles storage and rendering of ANSI-decorated single characters.
    """

    def __init__(self, pos=(0, 0), char=' ', **kwargs):
        """Segment __init__ method.

        Args:
            pos (tuple, optional): (y, x) position. Defaults to (0, 0).
            char (str, optional): Single char str. Defaults to ' '.
            **fg (str): Foreground Color key. Defaults to 'default'.
            **bg (str): Background Color key. Defaults to 'default'.

        Raises:
            TypeError: If pos is not tuple.
            ValueError: If pos does not contain 2 coords (y, x).
            ValueError: If char is not exactly length 1.

        """
        # check arguments are valid
        if not isinstance(pos, tuple):
            raise TypeError('pos is not tuple')
        if len(pos) < 2:
            raise ValueError('pos: too few coordinates given')

        if len(char) > 1 or len(char) <= 0:
            raise ValueError('char is wrong length.')

        # get optional arguments
        fg = kwargs.get('fg', 'default')  # foreground color of char
        bg = kwargs.get('bg', 'default')  # background color of char

        self.pos = pos
        self.char = char
        # control character libraries
        self.fgs = {
            'black'  : "30",
            'red'    : "31",
            'green'  : "32",
            'yellow' : "33",
            'blue'   : "34",
            'magenta': "35",
            'cyan'   : "36",
            'white'  : "37",

            'reset'  : "39",
            'default': "37"
        }
        self.bgs = {
            'black'  : "40",
            'red'    : "41",
            'green'  : "42",
            'yellow' : "43",
            'blue'   : "44",
            'magenta': "45",
            'cyan'   : "46",
            'white'  : "47",

            'reset'  : "49",
            'default': "40"
        }
        self.fg = self.fgs['default']
        self.bg = self.bgs['default']
        self.setfg(fg)
        self.setbg(bg)

    def setcharacter(self, char=' '):
        """Set new character.

        Args:
            char (str, optional): Single character str. Defaults to ' '.

        Raises:
            ValueError: If char is not exactly length 1

        Returns:
            str: The new character

        """
        if len(char) > 1 or len(char) <= 0:
            raise ValueError('char is wrong length.')

        self.char = char
        return char

    def setfg(self, fg='default'):
        """Set new Foreground Color.

        Args:
            fg (str, optional): New color key or value. Defaults to 'default'.

        Raises:
            ValueError: If fg arg is not supported color key or value.

        Returns:
            str: New color value

        """
        try:
            self.fg = self.fgs[fg]
        except KeyError:
            if fg in self.fgs.values():
                self.fg = fg
            else:
                raise ValueError('argument is not supported fg.')

        return self.fg

    def setbg(self, bg='default'):
        """Set new Background Color.

        Args:
            bg (str, optional): New color key or value. Defaults to 'default'.

        Raises:
            ValueError: If bg arg is not supported color key or value.

        Returns:
            str: New color value

        """
        try:
            self.bg = self.bgs[bg]
        except KeyError:
            if bg in self.bgs.values():
                self.bg = bg
            else:
                raise ValueError('argument is not supported bg.')

        return self.bg

    def setpos(self, pos=(0, 0)):
        """Set new segment position.

        Args:
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).

        Raises:
            TypeError: If pos is not tuple.
            ValueError: If pos does not contain 2 coords (y, x)

        Returns:
            tuple: New position

        """
        if not isinstance(pos, tuple):
            raise TypeError('argument is not tuple')
        if len(pos) < 2:
            raise ValueError('too few coordinates given')

        self.pos = pos
        return self.pos

    def configure(self, pos=None, char=None, **kwargs):
        """Configure segment.

        Changes pos, char, fg and bg.

        Args:
            pos (tuple, optional): (y, x) coordinates. Defaults to None.
            char (str, optional): Single char str. Defaults to None.
            **fg (str): Foreground Color key. Defaults to 'default'.
            **bg (str): Background Color key. Defaults to 'default'.

        Returns:
            bool: Returns True for verification.

        """
        # get optional arguments
        fg = kwargs.get('fg', None)  # foreground color of char
        bg = kwargs.get('bg', None)  # background color of char

        if pos is None:
            pos = self.pos
        if char is None:
            char = self.char
        if fg is None:
            fg = self.fg
        if bg is None:
            bg = self.bg

        self.setpos(pos)
        self.setcharacter(char)
        self.setfg(fg)
        self.setbg(bg)

        return True

    def __str__(self):
        """Format into str with ANSI decorators for use in compositor.

        Returns:
            str: Formatted str.

        """
        ret = "{}{};{}m{}{}".format(
            "\033[", self.fg, self.bg, self.char, "\033[0m")

        return ret
