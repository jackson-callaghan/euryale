"""Box Class.

Mostly used as a base class to inherit for more complex boxtypes. Contains
attributes and methods for storing and rendering a simple box with a few
fancy bits.

"""
from .segment import Segment
import math


class Box:
    """Box Class.

    Mostly used as a base class to inherit for more complex boxtypes. Contains
    attributes and methods for storing and rendering a simple box with a few
    fancy bits. Doesn't support colors from initialization, but they can be set
    after through internal methods.

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
            **ytarget (Box): vertical alignment target (can be compositor).
                Defaults to None.
            **ytalign (str): type of alignment to target vertically
            **ysalign (str): type of alignment to self vertically
            **xtarget (Box) horizontal alignment target (can be compositor).
                Defaults to None.
            **xtalign (str): type of alignment to target horizontally
            **xsalign (str): type of alignment to self horizontally


        Raises:
            TypeError: If pos is not tuple.
            ValueError: If pos does not contain two (y, x) coordinates.
            TypeError: If size is not tuple.
            ValueError: If size does not contain two (w, h) measures.
            ValueError: If splash does not fit size of box.

        """
        self.ytalign_possible = [
            "otop",
            "obottom",
            "top",
            "bottom",
            "itop",
            "ibottom",
            "center"
        ]
        self.ysalign_possible = [
            "above",
            "below",
            "top",
            "bottom",
            "center"
        ]
        self.xtalign_possible = [
            "left",
            "right",
            "oleft",
            "oright",
            "ileft",
            "iright",
            "center"
        ]
        self.xsalign_possible = [
            "oleft",
            "aleft",
            "oright",
            "aright",
            "center"
        ]

        dchar = kwargs.get('dchar', ' ')
        splash = kwargs.get('splash', None)
        overlay = kwargs.get('overlay', False)

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

        self._pos = pos
        self.ytarget = kwargs.get("ytarget", None)
        self.ytalign = kwargs.get("ytalign", "center")
        self.ysalign = kwargs.get("ysalign", "center")
        self.xtarget = kwargs.get("xtarget", None)
        self.xtalign = kwargs.get("xtalign", "center")
        self.xsalign = kwargs.get("xsalign", "center")
        self.size = size
        self.dchar = dchar
        self.parent = parent  # might be useful for some things
        self.name = name  # name is handled by compositor
        self.overlay = overlay  # overlay is handled by compositor

        self.populate()

        # TODO error checking for alignment and such

        if splash is not None:
            if len(splash) != size[0] or len(splash[0]) != size[1]:
                raise ValueError('splash: given splash does not fit size')
            else:
                self.from_splash(splash)

        self.setarea(c1=(0, 0),
                     c2=(self.size[0], self.size[1]),
                     char=self.dchar)

    @property
    def pos(self):
        """Get position based on set position and/or alignment targets.

        Returns:
            tuple: (y, x) coordinates.

        """
        y = 0
        x = 0
        # here comes the worst cluster of elif statements ever
        if self.ytarget is not None:
            h = self.size[0]
            ty = self.ytarget.pos[0]
            th = self.ytarget.size[0]

            if self.ytalign == "otop":
                y = ty - 1
            elif self.ytalign == "top":
                y = ty
            elif self.ytalign == "itop":
                y = ty + (1 if h > 2 else 0)
            elif self.ytalign == "center":
                y = ty + math.floor(th / 2)
            elif self.ytalign == "ibottom":
                y = ty + th - (2 if h > 2 else 1)
            elif self.ytalign == "bottom":
                y = ty + th - 1
            elif self.ytalign == "obottom":
                y = ty + th

            if self.ysalign == "above":
                y -= h if (th % 2 != 0 or self.ytalign != "center") else h + 1
            elif self.ysalign == "bottom":
                y -= (h - 1) if (th %
                                 2 != 0 or self.ytalign != "center") else h
            elif self.ysalign == "center":
                y -= math.floor(h / 2) - (1 if "bottom" in self.ytalign else 0)
            elif self.ysalign == "top":
                y = y  # change nothing
            elif self.ysalign == "below":
                y += 1

        if self.xtarget is not None:
            w = self.size[1]
            tx = self.xtarget.pos[1]
            tw = self.xtarget.size[1]

            if self.xtalign == "oleft":
                x = tx - 1
            elif self.xtalign == "left":
                x = tx
            elif self.xtalign == "ileft":
                x = tx + (1 if w > 2 else 0)
            elif self.xtalign == "center":
                x = tx + math.floor(tw / 2)
            elif self.xtalign == "iright":
                x = tx + tw - (2 if w > 2 else 1)
            elif self.xtalign == "right":
                x = tx + tw - 1
            elif self.xtalign == "oright":
                x = tx + tw

            if self.xsalign == "oright":
                x -= w if (tw % 2 != 0 or self.xtalign != "center") else w + 1
            elif self.xsalign == "aright":
                x -= (w - 1) if (tw %
                                 2 != 0 or self.xtalign != "center") else w
            elif self.xsalign == "center":
                x -= math.floor(w / 2) - (1 if "right" in self.xtalign else 0)
            elif self.xsalign == "aleft":
                x = x  # change nothing
            elif self.xsalign == "oleft":
                x += 1

        # position is either returned or used as offset for alignment
        y += self._pos[0]
        x += self._pos[1]

        return (y, x)

    @pos.setter
    def pos(self, pos):
        if not isinstance(pos, tuple):
            raise TypeError('argument is not tuple')
        if len(pos) < 2:
            raise ValueError('too few coordinates given')
        self._pos = pos

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

    def resize(self, newsize):
        """Resize the box.

        Args:
            newsize (tuple): (height, width) size.
        """
        grid = self.grid
        if newsize <= self.size:
            grid = [i[0:newsize[1]] for i in grid[0:newsize[0]]]
        splashgrid = grid
        for y, line in enumerate(grid):
            for x, seg in enumerate(line):
                splashgrid[y][x] = (seg.char, seg.fg, seg.bg)
        self.grid = []
        self.segments = []
        self.size = newsize
        self.populate()
        self.from_splash(splashgrid)

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
                pos, char=char, fg=fg, bg=bg)

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
                self.setsegment((y, x), char=char, fg=fg, bg=bg)

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
