"""Box Class.

Mostly used as a base class to inherit for more complex boxtypes. Contains
attributes and methods for storing and rendering a simple box with a few
fancy bits.

"""
from segment import Segment


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
            'black'  : "30",
            'red'    : "31",
            'green'  : "32",
            'yellow' : "33",
            'blue'   : "34",
            'magenta': "35",
            'cyan'   : "36",
            'white'  : "37",

            'reset'  : "0",
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

            'reset'  : "0",
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
