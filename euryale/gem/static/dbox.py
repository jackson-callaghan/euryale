"""Dynamic box.

Allows definition of points which are used to dynamically draw a box using
box drawing characters of customizable style. Allows for splits, etc.

"""
from .box import Box


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
            **defaultpoints (bool): Set points in corners. Defaults to 'False'.
            **ytarget (Box): vertical alignment target (can be compositor).
                Defaults to None.
            **ytalign (str): type of alignment to target vertically
            **ysalign (str): type of alignment to self vertically
            **xtarget (Box) horizontal alignment target (can be compositor).
                Defaults to None.
            **xtalign (str): type of alignment to target horizontally
            **xsalign (str): type of alignment to self horizontally

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

        overlay = kwargs.get('overlay', False)
        points = kwargs.get('points', None)
        style = kwargs.get('style', 'default')
        ytarget = kwargs.get("ytarget", None)
        ytalign = kwargs.get("ytalign", "center")
        ysalign = kwargs.get("ysalign", "center")
        xtarget = kwargs.get("xtarget", None)
        xtalign = kwargs.get("xtalign", "center")
        xsalign = kwargs.get("xsalign", "center")

        super().__init__(
            parent,
            name,
            pos=pos,
            size=size,
            overlay=overlay,
            ytarget=ytarget,
            ytalign=ytalign,
            ysalign=ysalign,
            xtarget=xtarget,
            xtalign=xtalign,
            xsalign=xsalign
        )

        if points is None:
            self.points = []
        else:
            self.points = [p for p in points]

        self._style = self.styles['default']
        self.style = (style, True)

        fg = kwargs.get('fg', 'default')
        bg = kwargs.get('bg', 'default')
        self.fg = (fg, True)
        self.bg = (bg, True)
        defaultpoints = kwargs.get('defaultpoints', False)

        if defaultpoints:
            self.default_points()

        if len(self.points) > 0:
            self.update()

    @property
    def fg(self):
        """Get the foreground color. Set the foreground color by name or value.

        Returns:
            str: the current foreground color code.

        """
        return self._fg

    @fg.setter
    def fg(self, value):

        if isinstance(value, tuple):
            fg, silent = value
        else:
            fg = value
            silent = False

        try:
            self._fg = self.fgs[fg]
        except KeyError:
            if fg in self.fgs.values():
                self._fg = fg
            else:
                raise ValueError("argument '{}' is not supported fg.".format(
                    fg))

        if not silent:
            self.update()

        return self.fg

    @property
    def bg(self):
        """Get the background color. Set the background color by name or value.

        Returns:
            str: the current background color code

        """
        return self._bg

    @bg.setter
    def bg(self, value):

        if isinstance(value, tuple):
            bg, silent = value
        else:
            bg = value
            silent = False

        try:
            self._bg = self.bgs[bg]
        except KeyError:
            if bg in self.bgs.values():
                self._bg = bg
            else:
                raise ValueError("argument '{}' is not supported bg.".format(
                    bg))

        if not silent:
            self.update()

        return self.bg

    def default_points(self):
        """Add default points to the dbox.

        Default points are the four corners.
        """
        self.addpoints(
            (0, 0),
            (self.size[0] - 1, 0),
            (0, self.size[1] - 1),
            (self.size[0] - 1, self.size[1] - 1),
            silent=True
        )

    def resize(self, newsize, rm_oldpoints=False, defaultpoints=False):
        """Resize the box.

        Args:
            newsize (tuple): (height, width) size.
        """
        self.grid = []
        self.segments = []
        self.size = newsize
        self.populate()

        if rm_oldpoints:
            self.points = []
        else:
            for point in [p for p in self.points]:
                if point > (self.size[0] - 1, self.size[1] - 1):
                    self.removepoint(point, True)

        if defaultpoints:
            self.default_points()

        self.update()

    def addpoint(self, pos=(0, 0), silent=False):
        """Add a point to box.

        Args:
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).
            silent (bool, optional): Skip updating. Defaults to False.

        Raises:
            TypeError: If pos is not tuple.
            ValueError: If pos does not contain 2 (y, x) coordinates.

        """
        if not isinstance(pos, tuple):
            raise TypeError('argument is not tuple')
        if len(pos) < 2:
            raise ValueError('too few coordinates given')

        self.points.append(pos)
        if not silent:
            self.update()

    def addpoints(self, *args, **kwargs):
        """Add multiple points.

        Args:
            *args (tuple): Arbitrary amount of (y, x) point arguments.
            **silent (bool): Skip updating. Defaults to False.

        """
        silent = kwargs.get("silent", False)
        for i in args:
            if i not in self.points:
                self.addpoint(i, True)
        if not silent:
            self.update()

    def removepoint(self, pos=(0, 0), silent=False):
        """Remove a point, selected by coordinates.

        Args:
            pos (tuple, optional): (y, x) coordinates. Defaults to (0, 0).
            silent (bool, optional): Skip updating. Defaults to False.

        Raises:
            TypeError: If pos is not tuple.
            ValueError: If pos does not contain 2 (y, x) coordinates

        """
        if not isinstance(pos, tuple):
            raise TypeError('argument is not tuple')
        if len(pos) < 2:
            raise ValueError('too few coordinates given')

        for i, p in enumerate([p for p in self.points]):
            if p == pos:
                self.points.pop(i)
        if not silent:
            self.update()

    def removepoints(self, *args):
        """Remove multiple points.

        Args:
            *args (tuple): Arbitrary amount of (y, x) point arguments.

        """
        for i in args:
            self.removepoint(i, True)
        self.update()

    @property
    def style(self):
        """Get the line style. Set the line style by name or value.

        Returns:
            str: the current style value.

        """
        return self._style

    @style.setter
    def style(self, value):

        try:
            style, silent = value
        except ValueError:
            style = value
            silent = False

        try:
            self._style = self.styles[style]
        except KeyError:
            if style in self.styles.values():
                self._style = style
            else:
                raise ValueError('argument is not supported style.')

        if not silent:
            self.update()

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

        self.pos = pos
        self.style = (style, True)
        self.fg = (fg, True)
        self.bg = (bg, True)
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

        self.setarea((0, 0), self.size, char=' ', fg=self.fg, bg=self.bg)

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
