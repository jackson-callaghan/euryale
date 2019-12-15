"""Static Compositor and associated Boxtypes.

Box-based compositor with no animations or interactive elements. Absolutely
the most bare-bones system, really used as the skeleton for Dynamic Compositor
(dynamic.py).

TODO: expand Chars list
TODO: diagonal corners for DBox
TODO: EBox: edge-defined DBox (allows for multiple styles per edge, matched corners)
TODO: ETBox: edge-defined TBox
"""

import os
import sys
import textwrap

from colorama import init as fgama_init  # used to support ANSI in windows cmd

# import logging
# In case I have to bugfix, quick logging here:
# logging.basicConfig(filename='SAILR.log', level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.propagate = False
# logger.addHandler(logging.FileHandler('SAILR.log', 'w'))

# logging.info('program started')

fgama_init(autoreset=False)


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
            'black': "30",
            'red': "31",
            'green': "32",
            'yellow': "33",
            'blue': "34",
            'magenta': "35",
            'cyan': "36",
            'white': "37",

            'reset': "39",
            'default': "37"
        }
        self.bgs = {
            'black': "40",
            'red': "41",
            'green': "42",
            'yellow': "43",
            'blue': "44",
            'magenta': "45",
            'cyan': "46",
            'white': "47",

            'reset': "49",
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


class Box:
    """Box Class.

    Mostly used as a base class to inherit for more complex boxtypes. Contains
    attributes and methods for storing and rendering a simple box with a few
    fancy bits.

    """

    def __init__(self, parent, name, pos=(0, 0), size=(0, 0), **kwargs):
        """Box __init__ method.

        Args:
            parent (Compositor): Compositor that owns this box.
            name (str): Name of box.
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).
            size (tuple, optional): (height, width) size. Defaults to (0, 0).
            **dchar (str): default single character to fill box.
            **splash (list): 2d list of str or tuple with char, fg and bg
                defining a premade box fill.
            **overlay (bool): Show boxes below through blank chars. Defaults to
                False.

        Raises:
            TypeError: If pos is not tuple.
            ValueError: If pos does not contain two (y, x) coordinates.
            TypeError: If size is not tuple.
            ValueError: If size does not contain two (w, h) measures.
            ValueError: If splash does not fit size of box.

        """
        self.fgs = {
            'black': "30",
            'red': "31",
            'green': "32",
            'yellow': "33",
            'blue': "34",
            'magenta': "35",
            'cyan': "36",
            'white': "37",

            'reset': "0",
            'default': "37"
        }
        self.bgs = {
            'black': "40",
            'red': "41",
            'green': "42",
            'yellow': "43",
            'blue': "44",
            'magenta': "45",
            'cyan': "46",
            'white': "47",

            'reset': "0",
            'default': "40"
        }

        dchar = kwargs.get('dchar', ' ')
        splash = kwargs.get('splash', None)
        overlay = kwargs.get('overlay', False)
        fg = kwargs.get('fg', 'default')
        bg = kwargs.get('bg', 'default')

        self.segments = []
        self.grid = []
        # check arguments are valid
        if not isinstance(pos, tuple):
            raise TypeError('pos is not tuple')
        if len(pos) < 2:
            raise ValueError('pos: too few coordinates given')

        if not isinstance(size, tuple):
            raise TypeError('size is not tuple')
        if len(size) < 2:
            raise ValueError('size: too few coordinates given')

        self.pos = pos
        self.size = size
        self.dchar = dchar
        self.parent = parent  # might be useful for some things
        self.name = name  # name is handled by compositor
        self.overlay = overlay  # overlay is handled by compositor

        self.populate()

        if splash is not None:
            if len(splash) != size[0] or len(splash[0]) != size[1]:
                raise ValueError('splash: given splash does not fit size')
            else:
                self.from_splash(splash)

        self.fg = self.fgs[fg]
        self.bg = self.bgs[bg]

        self.setarea(c1=(0, 0),
                     c2=(self.size[0], self.size[1]),
                     char=self.dchar,
                     fg=self.fg,
                     bg=self.bg)

    def populate(self):
        """Populate grid with default character segments.

        Returns:
            list: New grid, 2d list of segments.

        """
        for y in range(self.size[0]):
            self.grid.append([])
            for x in range(self.size[1]):
                self.grid[y].append(Segment((y, x), self.dchar))
                self.segments.append(self.grid[y][x])

        return self.grid

    def setsegment(self, pos=(0, 0), char=None, **kwargs):
        """Configure a single segment.

        Args:
            pos (tuple, optional): (y, x) coordinates to select segment from
                grid. Defaults to (0, 0).
            char (str, optional): Single character str. Defaults to None.
            **fg (str): Foreground Color key. Defaults to 'default'.
            **bg (str): Background Color key. Defaults to 'default'.

        """
        fg = kwargs.get('fg', None)  # foreground color
        bg = kwargs.get('bg', None)  # background color

        if all((  # provided segment exists
                pos[0] <= len(self.grid) - 1,
                pos[1] <= len(self.grid[0]) - 1)
               ):
            self.grid[pos[0]][pos[1]].configure(
                pos, char, fg=fg, bg=bg)

    def from_splash(self, splash):
        """Set grid from a splash.

        Args:
            splash (list): 2d list of str or tuple of char, fg, bg.

        Returns:
            list: New grid, 2d list of segments

        """
        for y, line in enumerate(splash):
            for x, c in enumerate(line):
                # can take character or tuple with char, fg, and bg
                if len(c) > 2:
                    self.setsegment((y, x), c[0], fg=c[1], bg=c[2])
                elif len(c) > 1:
                    self.setsegment((y, x), c[0])
                else:
                    self.setsegment((y, x), c[0])
        return self.grid

    def splash_area(self, splash, c1=(0, 0), c2=(0, 0)):
        """Set a splash over a specific area of box.

        Args:
            splash (list): 2d list of str or tuple of char, fg, bg
            c1 (tuple, optional): First corner of area in form (y, x).
                Defaults to (0, 0).
            c2 (tuple, optional): Second corner of area in form (y, x).
                Defaults to (0, 0).

        Returns:
            list: New grid, 2d list of segments.

        """
        # get corner coords (mostly for readability)
        y1 = c1[0]
        x1 = c1[1]

        y2 = c1[0] + c2[0] - 1
        x2 = c1[1] + c2[1] - 1

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                char = splash[y - y1][x - x1]
                if len(char) > 2:  # can take str or tuple of char, fg, bg
                    self.setsegment((y, x), char[0], fg=char[1], bg=char[2])
                elif isinstance(char, tuple):
                    self.setsegment((y, x), char[0])
                else:
                    self.setsegment((y, x), char)

        return self.grid

    def setpos(self, pos=(0, 0)):
        """Set new position for box.

        Args:
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).

        Raises:
            TypeError: If pos is not tuple.
            ValueError: If pos does not contain 2 (y, x) coordinates.

        Returns:
            tuple: New position.

        """
        if not isinstance(pos, tuple):
            raise TypeError('argument is not tuple')
        if len(pos) < 2:
            raise ValueError('too few coordinates given')

        self.pos = pos

        return self.pos

    def setarea(self, c1=(0, 0), c2=(0, 0), char=None, **kwargs):
        """Replace an area of the box with a given character.

        Args:
            c1 (tuple, optional): First corner (y, x). Defaults to (0, 0).
            c2 (tuple, optional): Second corner (y, x). Defaults to (0, 0).
            char (str, optional): Single character str. Defaults to None.
            **fg (str): Foreground Color key. Defaults to 'default'.
            **bg (str): Background Color key. Defaults to 'default'.

        Returns:
            list: New grid, 2d list of segments.

        """
        fg = kwargs.get('fg', None)
        bg = kwargs.get('bg', None)

        # first and second corner coords, mostly for readability
        y1 = c1[0]
        x1 = c1[1]

        y2 = c2[0]
        x2 = c2[1]

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.setsegment((y, x), char, fg=fg, bg=bg)

        return self.grid

    def rectangle(self, c1=(0, 0), c2=(0, 0), char=None, **kwargs):
        """Replace a rectangular area of box.

        Includes options to only set a stroke edge, and to add inlay to that.

        Args:
            c1 (tuple, optional): First corner (y, x). Defaults to (0, 0).
            c2 (tuple, optional): Second corner (y, x). Defaults to (0, 0).
            char (str, optional): Single character str. Defaults to None.
            **stroke (int): Thickness of stroke. 0 disables stroke.
                Defaults to 0.
            **inlay (str): Character to replace inside box made by stroke.
                False disables inlay. Defaults to False.
            **fg (str): Foreground Color key. Defaults to 'default'.
            **bg (str): Background Color key. Defaults to 'default'.
            **inlay_fg (str): Inlay Foreground Color key.
                Defaults to 'default'.
            **inlay_bg (str): Inlay Background Color key.
                Defaults to 'default'.

        """
        stroke = kwargs.get('stroke', 0)
        inlay = kwargs.get('inlay', False)
        fg = kwargs.get('fg', None)
        bg = kwargs.get('bg', None)
        inlay_fg = kwargs.get('inlay_fg', None)
        inlay_bg = kwargs.get('inlay_bg', None)

        self.setarea(c1, c2, char, fg=fg, bg=bg)

        dy = c2[0] - c1[0]
        dx = c2[1] - c1[0]

        # set area inside stroke to either blank or inlay
        if stroke > 0 and all((dy > 2, dx > 2)):
            s_pos = (c1[0] + stroke, c1[1] + stroke)
            s_size = (c2[0] - stroke, c2[1] - stroke)
            s_char = ' ' if not inlay else inlay
            self.setarea(s_pos, s_size, s_char, fg=inlay_fg, bg=inlay_bg)

    def __str__(self):
        """Return str that summarizes box details.

        Returns:
            str: Summary of box details.

        """
        return "Box '{}' of size ({}, {}) at ({}, {}), overlay {}".format(
            self.name, self.size[0], self.size[1], self.pos[0], self.pos[1],
            str(self.overlay))


class DBox(Box):
    """Dynamic box.

    Allows definition of points which are used to dynamically draw a box using
    box drawing characters of customizable style. Allows for splits, etc.

    """

    def __init__(self, parent, name, pos=(0, 0), size=(0, 0), **kwargs):
        """Dynamic Box __init__ method.

        Args:
            parent (Compositor): Compositor that owns this DBox.
            name (str): Name of box for reference.
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).
            size (tuple, optional): (height, width) size. Defaults to (0, 0).
            **overlay (bool): Show boxes below through blank chars. Defaults to
                False.
            **points (list): List of (y, x) tuples defining points at init.
            **style (str): Style key for box drawing characters.
            **fg (str): Foreground Color key. Defaults to 'default'.
            **bg (str): Background Color key. Defaults to 'default'.

        """
        overlay = kwargs.get('overlay', False)
        points = kwargs.get('points', None)
        style = kwargs.get('style', 'default')
        fg = kwargs.get('fg', 'default')
        bg = kwargs.get('bg', 'default')

        super().__init__(parent, name, pos, size, overlay=overlay)
        if points is None:
            self.points = []
        else:
            self.points = [p for p in points]

        self.styles = {
            'default': "─│┌┐└┘├┤┬┴┼",
            'singlelight': "─│┌┐└┘├┤┬┴┼",
            'singleround': "─│╭╮╰╯├┤┬┴┼",
            'singleheavy': "━┃┏┓┗┛┣┫┳┻╋",
            'double': "═║╔╗╚╝╠╣╦╩╬",
            'dash2light': "╌╎┌┐└┘├┤┬┴┼",
            'dash2heavy': "╍╏┏┓┗┛┣┫┳┻╋",
            'dash3light': "┄┆┌┐└┘├┤┬┴┼",
            'dash3heavy': "┅┇┏┓┗┛┣┫┳┻╋",
            'dash4light': "┈┊┌┐└┘├┤┬┴┼",
            'dash4heavy': "┉┋┏┓┗┛┣┫┳┻╋",
            'dash2round': "╌╎╭╮╰╯├┤┬┴┼",
            'dash3round': "┄┆╭╮╰╯├┤┬┴┼",
            'dash4round': "┈┊╭╮╰╯├┤┬┴┼",
            'blockshadel': "░░░░░░░░░░░",
            'blockshadem': "▒▒▒▒▒▒▒▒▒▒▒",
            'blockshaded': "▓▓▓▓▓▓▓▓▓▓▓",
            'fullblock': "███████████"
        }

        self.style = self.styles['default']
        self.fg = self.fgs['default']
        self.bg = self.bgs['default']
        self.setstyle(style, True)
        self.setfg(fg, True)
        self.setbg(bg, True)

        if len(self.points) > 0:
            self.update()

    def addpoint(self, pos=(0, 0), s=False):
        """Add a point to box.

        Args:
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).
            s (bool, optional): Skip updating. Defaults to False.

        Raises:
            TypeError: If pos is not tuple.
            ValueError: If pos does not contain 2 (y, x) coordinates.

        """
        if not isinstance(pos, tuple):
            raise TypeError('argument is not tuple')
        if len(pos) < 2:
            raise ValueError('too few coordinates given')

        self.points.append(pos)
        if not s:
            self.update()

    def addpoints(self, *args):
        """Add multiple points.

        Args:
            *args (tuple): Arbitrary amount of (y, x) point arguments.

        """
        for i in args:
            if i not in self.points:
                self.addpoint(i, True)
        self.update()

    def removepoint(self, pos=(0, 0), s=False):
        """Remove a point, selected by coordinates.

        Args:
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).
            s (bool, optional): Skip updating. Defaults to False.

        Raises:
            TypeError: If pos is not tuple.
            ValueError: If pos does not contain 2 (y, x) coordinates

        """
        if not isinstance(pos, tuple):
            raise TypeError('argument is not tuple')
        if len(pos) < 2:
            raise ValueError('too few coordinates given')

        for i, p in enumerate([p for p in self.points]):
            if p[0] == pos[0] and p[1] == pos[1]:
                self.points.pop(i)
        if not s:
            self.update()

    def removepoints(self, *args):
        """Remove multiple points.

        Args:
            *args (tuple): Arbitrary amount of (y, x) point arguments.

        """
        for i in args:
            self.removepoint(i, True)
        self.update()

    def setstyle(self, style='default', s=False):
        """Set style of box drawing characters to use.

        Args:
            style (str, optional): Style key or value. Defaults to 'default'.
            s (bool, optional): Skip updating. Defaults to False.

        Raises:
            ValueError: If style is not valid style key or value.

        Returns:
            str: New style.

        """
        try:
            self.style = self.styles[style]
        except KeyError:
            if style in self.styles.values():
                self.style = style
            else:
                raise ValueError('argument is not supported style.')

        if not s:
            self.update()

        return self.style

    def setfg(self, fg='default', s=False):
        """Set new Foreground Color.

        Args:
            fg (str, optional): Foreground Color key or value.
                Defaults to 'default'.
            s (bool, optional): Skip updating. Defaults to False.

        Raises:
            ValueError: If fg is not valid color key or value.

        Returns:
            str: New Foreground Color

        """
        try:
            self.fg = self.fgs[fg]
        except KeyError:
            if fg in self.fgs.values():
                self.fg = fg
            else:
                raise ValueError('argument is not supported fg.')

        if not s:
            self.update()

        return self.fg

    def setbg(self, bg='default', s=False):
        """Set new Background Color.

        Args:
            bg (str, optional): Background Color key or value.
                Defaults to 'default'.
            s (bool, optional): Skip updating. Defaults to False.

        Raises:
            ValueError: If bg is not valid color key or value.

        Returns:
            str: New Background Color

        """
        try:
            self.bg = self.bgs[bg]
        except KeyError:
            if bg in self.bgs.values():
                self.bg = bg
            else:
                raise ValueError('argument is not supported bg.')

        if not s:
            self.update()

        return self.bg

    def configure(self, pos=None, **kwargs):
        """Configure DBox.

        Can set new pos, style, fg, and bg.

        Args:
            pos (tuple, optional): (y, x) coordinates. Defaults to None.
            **style (str): Style key for box drawing characters.
            **fg (str): Foreground Color key. Defaults to 'default'.
            **bg (str): Background Color key. Defaults to 'default'.

        Returns:
            bool: Returns True for verification.

        """
        style = kwargs.get('style', None)
        fg = kwargs.get('fg', None)
        bg = kwargs.get('bg', None)

        if pos is None:
            pos = self.pos
        if style is None:
            style = self.style
        if fg is None:
            fg = self.fg
        if bg is None:
            bg = self.bg

        self.setpos(pos)
        self.setstyle(style, True)
        self.setfg(fg, True)
        self.setbg(bg, True)
        self.update()

        return True

    def update(self):
        """Update drawn boxes."""
        def isint(obj):
            """Check if obj is int.

            Helper function.

            Args:
                obj (object): An object

            Returns:
                bool: True if obj is int else False

            """
            return True if not isinstance(obj, bool) else False

        self.setarea((0, 0), self.size, ' ', fg=self.fg, bg=self.bg)

        for point in self.points:
            y = point[0]
            x = point[1]

            try:
                nlx = max(
                    [p[1] for p in self.points if p[0] == y and p[1] < x])
            except ValueError:
                nlx = False
            try:
                nuy = max(
                    [p[0] for p in self.points if p[1] == x and p[0] < y])
            except ValueError:
                nuy = False
            try:
                nrx = min(
                    [p[1] for p in self.points if p[0] == y and p[1] > x])
            except ValueError:
                nrx = False
            try:
                ndy = min(
                    [p[0] for p in self.points if p[1] == x and p[0] > y])
            except ValueError:
                ndy = False

            # set character for vertex and set area to next verticies
            count = 0
            selector = {
                1100: self.style[2],
                1001: self.style[3],
                110: self.style[4],
                11: self.style[5],
                1110: self.style[6],
                1011: self.style[7],
                1101: self.style[8],
                111: self.style[9],
                1111: self.style[10],
                1010: self.style[1],
                101: self.style[0]
            }

            if isint(nlx):
                self.setarea(
                    (y, nlx + 1), (y, x - 1), self.style[0], fg=self.fg,
                    bg=self.bg)
                count += 1
            if isint(nuy):
                self.setarea(
                    (nuy + 1, x), (y - 1, x), self.style[1], fg=self.fg,
                    bg=self.bg)
                count += 10
            if isint(nrx):
                self.setarea(
                    (y, x + 1), (y, nrx - 1), self.style[0], fg=self.fg,
                    bg=self.bg)
                count += 100
            if isint(ndy):
                self.setarea(
                    (y + 1, x), (ndy - 1, x), self.style[1], fg=self.fg,
                    bg=self.bg)
                count += 1000

            try:
                self.setsegment((y, x), selector[count], fg=self.fg,
                                bg=self.bg)
            except KeyError:
                continue


class TBox(DBox):
    """Text Box.

    Options for stripping newlines from input, as well as wrapping and box
    outline.

    """

    def __init__(self, parent, name=None, pos=(0, 0), size=(0, 0), **kwargs):
        """Text Box __init__ method.

        Args:
            parent (Compositor): Compositor that owns this TBox.
            name (str, optional): Name of box. Defaults to None.
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).
            size (tuple, optional): (height, width) size. Defaults to (0, 0).
            **text (object): Any object with a __str__ method to render.
                Defaults to ''.
            **wrap (bool): Wrap text in textbox. Defaults to False.
            **border (str): Style key or value for box border. False disables
                border. Defaults to False.
            **strip_newlines (bool): Strip newlines from text.
                Defaults to False.
            **overlay (bool): Show other boxes below through blank characters.
                Defaults to False.
            **fg (str): Foreground Color key. Defaults to 'default'.
            **bg (str): Background Color key. Defaults to 'default'.

        Raises:
            TypeError: If strip_newlines is not bool.
            TypeError: If wrap is not bool.

        """
        text = kwargs.get('text', '')
        wrap = kwargs.get('wrap', False)
        border = kwargs.get('border', False)
        strip_newlines = kwargs.get('strip_newlines', False)
        overlay = kwargs.get('overlay', False)
        fg = kwargs.get('fg', 'default')
        bg = kwargs.get('bg', 'default')
        # check arguments are valid
        if not isinstance(strip_newlines, bool):
            raise TypeError("strip_newlines is not bool")
        if not isinstance(wrap, bool):
            raise TypeError("wrap is not bool")
        super().__init__(parent=parent, name=name, pos=pos, size=size,
                         overlay=overlay, fg=fg, bg=bg)

        self.text = text
        self.wrap = wrap
        self.strip_newlines = strip_newlines

        self.setborder(border)
        self.update()

    def setwrap(self, wrap=False):
        """Set wrap option.

        Args:
            wrap (bool, optional): Wrap text in box. Defaults to False.

        Raises:
            TypeError: If wrap is not bool.

        Returns:
            bool: New wrap value.

        """
        if not isinstance(wrap, bool):
            raise TypeError('argument is not bool')
        self.wrap = wrap
        self.update()
        return self.wrap

    def toggle_wrap(self):
        """Toggle wrap option.

        Returns:
            bool: New wrap value.

        """
        self.wrap = not self.wrap
        self.update()
        return self.wrap

    def setborder(self, border=False):
        """Set border style.

        Args:
            border (str, optional): Style key or value for box border.
                Defaults to False.

        Raises:
            ValueError: [description]

        Returns:
            str: New border style.

        """
        if border is not False and (border not in self.styles.keys()
                                    and border not in self.styles.values()):
            raise ValueError('argument is not valid border style')

        self.border = border

        if self.border is not False:
            y1 = 0
            x1 = 0

            y2 = self.size[0] - 1
            x2 = self.size[1] - 1

            self.setstyle(self.border, True)
            self.addpoints((y1, x1), (y1, x2), (y2, x2), (y2, x1))

        return self.border

    def settext(self, text):
        """Set text to new object or str.

        Args:
            text (object): Any object with a __str__ method.

        """
        self.text = text
        self.update()

    def update(self):
        """Update TBox."""
        super().update()
        text = str(self.text)
        if self.strip_newlines:
            text = text.replace('\n', '')

        if self.wrap:
            if self.border is not False:
                wrapper = textwrap.TextWrapper(width=self.size[1] - 2)
                wrapped = wrapper.wrap(text)
            else:
                wrapper = textwrap.TextWrapper(width=self.size[1] - 2)
                wrapped = wrapper.wrap(text)

        else:
            wrapped = [text]

        for y, line in enumerate(wrapped):
            for x, c in enumerate(line):
                if all([y <= self.size[0] - 1, x <= self.size[1] - 1]):
                    if self.border is not False:
                        if y + 1 == self.size[0] - 1:
                            continue
                        else:
                            self.setsegment((y + 1, x + 1), char=c,
                                            fg=self.fg, bg=self.bg)
                    else:
                        self.setsegment((y, x), char=c,
                                        fg=self.fg, bg=self.bg)
                else:
                    break

    def __str__(self):
        """Return str format summarizing box.

        Returns:
            str: str format summarizing box.

        """
        ret = "Box '{}' of size ({}, {}) at ({}, {}), overlay {}\
            \nContains text:\n{}".format(
            self.name, self.size[0], self.size[1], self.pos[0], self.pos[1],
            str(self.overlay), str(self.text))
        return ret


class Compositor:
    """Static Compositor.

    For all your bare-bones compositing needs.

    """

    def __init__(self, size=(29, 120)):
        """Compositor __init__ method.

        Args:
            size (tuple, optional): (height, width) size. Controls size in
            terminal. Defaults to (29, 120).

        """
        self.size = size
        # ordered list of objects, order determines render order
        self.objectlist = []
        self.grid = []
        self.segments = []
        self.populate()
        self.blank = self.grid

    def populate(self):
        """Populate grid with blank segments.

        Returns:
            list: New grid, 2d list of segments.

        """
        for y in range(self.size[0]):
            self.grid.append([])
            for x in range(self.size[1]):
                self.grid[y].append(Segment((y, x)))
                self.segments.append(self.grid[y][x])

        return self.grid

    def clear(self):
        """Configure all segments in grid to be blank.

        Returns:
            list: Grid, 2d list of segments.

        """
        for s in self.segments:
            s.configure(pos=None, char=' ', fg='default', bg='default')

        return self.grid

    def place_object(self, obj, height):
        """Place a box at a given height in the compositor.

        Args:
            obj (Box): Box to be placed.
            height (int, str): int indicating specific location, str indicating
                top, bottom, or above/below <boxname>.


        Raises:
            ValueError: If box name given doesn't correspond to any existing
                box.

        """
        if height == 'top':
            self.objectlist.append(obj)
        elif height == 'bottom':
            self.objectlist.insert(0, obj)
        elif isinstance(height, int):
            self.objectlist.insert(height, obj)
        elif ' ' in height:
            arg = height.split(' ')
            # check if target argument exists and raise exception if not
            if arg[1] not in self.objectlist:
                raise ValueError('box name does not correspond to any in list')
            # place object either above or below target
            else:
                # select target object
                target = [o for o in self.objectlist if o.name == arg[1]][0]
                if arg[0] == 'above':
                    self.objectlist.insert(
                        self.objectlist.index(target) + 1, obj)
                elif arg[0] == 'below':
                    self.objectlist.insert(
                        self.objectlist.index(target) - 1, obj)

    def removeobject(self, objname=None):
        """Remove box by name.

        Args:
            objname (str, optional): Name of box to remove. Defaults to None.

        Returns:
            bool: False if nothing was removed, or True if something was.

        """
        if objname is None:
            return False
        if objname not in [i.name for i in self.objectlist]:
            return False  # instead of error because it's technically not there
        else:
            self.objectlist = [i for i in self.objectlist if i.name != objname]
            return True

    def makebox(self, name, pos=(0, 0), size=(0, 0), dchar=' ',
                splash=None, fg='default',  bg='default', overlay=False, height='top'
                ):
        """Make a new Box and add to compositor.

        Args:
            name (str, optional): Name of box. Defaults to None.
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).
            size (tuple, optional): (height, width) size. Defaults to (0, 0).
            dchar (str, optional): Default character to fill box.
                Defaults to ' '.
            splash (list, optional): 2d list of str or tuple of char, fg, bg.
                Defaults to None.
            overlay (bool, optional): Show boxes below through blank
                characters. Defaults to False.
            height (int, str, optional): Height of box. Defaults to 'top'.

        Returns:
            Box: New Box.

        """
        if name is None:
            name = 'box#{}'.format(len(self.objectlist))

        new = Box(self, name=name, pos=pos, size=size, dchar=dchar,
                  splash=splash, fg=fg, bg=bg, overlay=overlay)

        self.place_object(new, height)
        return new

    def makedbox(self, name, pos=(0, 0), size=(0, 0), points=None,
                 style='default', fg='default', bg='default', overlay=False,
                 height='top'):
        """Make a new DBox and add to compositor.

        Args:
            name (str, optional): Name of box. Defaults to None.
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).
            size (tuple, optional): (height, width) size. Defaults to (0, 0).
            points ([type], optional): [description]. Defaults to None.
            style (str, optional): [description]. Defaults to 'default'.
            fg (str, optional): Foreground Color key or value.
                Defaults to 'default'.
            bg (str, optional): Background Color key or value.
                Defaults to 'default'.
            overlay (bool, optional): Show boxes below through blank
                characters. Defaults to False.
            height (int, str, optional): Height of box. Defaults to 'top'.

        Returns:
            DBox: New DBox.

        """
        if name is None:
            name = 'dbox#{}'.format(len(self.objectlist))

        new = DBox(self, name=name, pos=pos, size=size, points=points,
                   style=style, fg=fg, bg=bg, overlay=overlay)

        self.place_object(new, height)
        return new

    def maketbox(self, name, pos=(0, 0), size=(0, 0), points=None,
                 style='default', fg='default', bg='default', overlay=False,
                 text='', wrap=False, border=False, height='top'):
        """Make a new TBox and add to compositor.

        Args:
            name (str, optional): Name of box. Defaults to None.
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).
            size (tuple, optional): (height, width) size. Defaults to (0, 0).
            points ([type], optional): [description]. Defaults to None.
            style (str, optional): [description]. Defaults to 'default'.
            fg (str, optional): Foreground Color key or value.
                Defaults to 'default'.
            bg (str, optional): Background Color key or value.
                Defaults to 'default'.
            overlay (bool, optional): Show boxes below through blank
                characters. Defaults to False.
            text (object, optional): Any object with __str__ method.
                Defaults to ''.
            wrap (bool, optional): Wrap text in box. Defaults to False.
            border (str, optional): Border style key or value. False disables
                border. Defaults to False.
            height (int, str, optional): Height of box. Defaults to 'top'.

        Returns:
            TBox: New TBox.

        """
        if name is None:
            name = 'tbox#{}'.format(len(self.objectlist))

        new = TBox(self, name=name, pos=pos, size=size, points=points,
                   style=style, fg=fg, bg=bg, text=text, wrap=wrap,
                   border=border, overlay=overlay)

        self.place_object(new, height)
        return new

    def setsegment(self, pos=(0, 0), char=None, fg=None, bg=None):
        """Configure a single segment, selected by position.

        Args:
            pos (tuple, optional): (y, x) coordinates.. Defaults to (0, 0).
            char (str, optional): Single character str. Defaults to None.
            fg (str, optional): Foreground Color key or value.
                Defaults to None.
            bg (str, optional): Background Color key or value.
                Defaults to None.

        """
        self.grid[pos[0]][pos[1]].configure(pos, char, fg=fg, bg=bg)

    def to_grid(self, obj):
        """Paint box to grid.

        Args:
            obj (Box): Any boxtype.

        Returns:
            list: Grid, 2d list of segments.

        """
        pos = obj.pos
        size = obj.size
        splash = obj.grid

        y1 = pos[0]
        x1 = pos[1]
        # get second corner coords
        y2 = pos[0] + size[0] - 1
        x2 = pos[1] + size[1] - 1

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                seg = splash[y - y1][x - x1]
                if obj.overlay:
                    if seg.char in ('', ' '):
                        self.setsegment((y, x), self.grid[y][x].char,
                                        self.grid[y][x].fg, seg.bg)
                    else:
                        self.setsegment((y, x), seg.char, seg.fg, seg.bg)
                else:
                    self.setsegment((y, x), seg.char, seg.fg, seg.bg)

        return self.grid

    def composite(self):
        """Composite all objects to grid and render to stdout."""
        self.clear()

        for o in self.objectlist:
            if isinstance(o, DBox):
                o.update()
            self.to_grid(o)

        self.render()

    def rout(self, grid):
        """Render a given grid.

        Args:
            grid (list): 2d list of segments.

        """
        os.system('cls' if os.name == 'nt' else 'clear')
        output = ""
        for y, line in enumerate(grid):
            for x, c in enumerate(line):
                output += str(c)

                if x >= self.size[1] - 1 and y < self.size[0]:
                    output += "\n"

        sys.stdout.write(output)
        sys.stdout.flush()

    def render(self):
        """Render compositor grid.

        Wrapper for rout().

        """
        self.rout(self.grid)

    def debug_render(self, grid):
        """Render given grid.

        Wrapper for rout() for debug purposes.

        Args:
            grid (list): 2d list of segments

        """
        self.rout(grid)


class Fore():
    """Foreground colors.

    Can use attributes as arguments or use the attribute name str in lowercase
    as arguments.

    """

    BLACK = '30'
    RED = '31'
    GREEN = '32'
    YELLOW = '33'
    BLUE = '34'
    MAGENTA = '35'
    CYAN = '36'
    WHITE = '37'
    RESET = '39'


class Back():
    """Background colors.

    Can use attributes as arguments or use the attribute name str in lowercase
    as arguments.

    """

    BLACK = '40'
    RED = '41'
    GREEN = '42'
    YELLOW = '43'
    BLUE = '44'
    MAGENTA = '45'
    CYAN = '46'
    WHITE = '47'
    RESET = '49'


class Style():
    """Style keys.

    Can use attributes as arguments or use the attribute name str in lowercase
    as arguments.

    """

    DEFAULT = "─│┌┐└┘├┤┬┴┼"
    SINGLELIGHT = "─│┌┐└┘├┤┬┴┼"
    SINGLEROUND = "─│╭╮╰╯├┤┬┴┼"
    SINGLEHEAVY = "━┃┏┓┗┛┣┫┳┻╋"
    DOUBLE = "═║╔╗╚╝╠╣╦╩╬"
    DASH2LIGHT = "╌╎┌┐└┘├┤┬┴┼"
    DASH2HEAVY = "╍╏┏┓┗┛┣┫┳┻╋"
    DASH3LIGHT = "┄┆┌┐└┘├┤┬┴┼"
    DASH4HEAVY = "┅┇┏┓┗┛┣┫┳┻╋"
    DASH4LIGHT = "┈┊┌┐└┘├┤┬┴┼"
    DASH4HEAVY = "┉┋┏┓┗┛┣┫┳┻╋"
    DASH2ROUND = "╌╎╭╮╰╯├┤┬┴┼"
    DASH3ROUND = "┄┆╭╮╰╯├┤┬┴┼"
    DASH4ROUND = "┈┊╭╮╰╯├┤┬┴┼"
    BLOCKSHADEL = "░░░░░░░░░░░"
    BLOCKSHADEM = "▒▒▒▒▒▒▒▒▒▒▒"
    BLOCKSHADED = "▓▓▓▓▓▓▓▓▓▓▓"
    FULLBLOCK = "███████████"


class Chars():
    """Commonly used characters.

    For accessing characters you might commonly use for whatever reason with
    greater ease than might be typical.
    """

    BLOCK_LIGHT = "░"
    BLOCK_MEDIUM = "▒"
    BLOCK_HEAVY = "▓"
    BLOCK_FULL = "█"
