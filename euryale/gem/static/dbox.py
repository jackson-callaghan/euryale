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

        self.pos = pos
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
