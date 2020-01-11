"""Static Compositor and associated Boxtypes.

Box-based compositor with no animations or interactive elements. Absolutely
the most bare-bones system, but good enough for basic purposes. Eventually to
be used as the basis for a dynamic version.

TODO: expand Chars list
TODO: diagonal corners for DBox
TODO: EBox: edge-defined DBox (allows for multiple styles per edge,
                               matched corners)
TODO: ETBox: edge-defined TBox
"""

import os
import sys
from .segment import Segment
from .box import Box
from .dbox import DBox
from .tbox import TBox

from colorama import init as fgama_init  # used to support ANSI in windows cmd

# import logging
# In case I have to bugfix, quick logging here:
# logging.basicConfig(filename='SAILR.log', level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.propagate = False
# logger.addHandler(logging.FileHandler('SAILR.log', 'w'))

# logging.info('program started')

fgama_init(autoreset=False)


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
        """Remove object by reference.

        Args:
            objname (str): Name of box to remove. Defaults to None.

        Returns:
            bool: False if nothing was removed, or True if something was.

        """
        if objname is None:
            return False
        if objname not in self.objectlist:
            return False  # instead of error because it's technically not there
        else:
            self.objectlist.remove(objname)
            return True

    def makebox(self, **kwargs):
        """Make a Box and place it in the object list.

        All arguments are technically optional.

        Args:
            **name (str): Name of box. Defaults to auto-generation via None.
            **pos (tuple): (y, x) coordinates. Defaults to (0, 0).
            **size (tuple): (height, width) size. Defaults to (0, 0).
            **dchar (str): default single character to fill box.
            **splash (list): 2d list of str or tuple with char, fg and bg
                defining a premade box fill.
            **fg (str): Foreground Color key. Defaults to 'default'.
            **bg (str): Background Color key. Defaults to 'default'.
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
            **height (str): height of object in objectlist, used for overlaps.

        Returns:
            Box: New Box.

        """
        name = kwargs.get("name", None)
        pos = kwargs.get("pos", (0, 0))
        size = kwargs.get("size", (1, 1))
        dchar = kwargs.get("dchar", ' ')
        splash = kwargs.get("splash", None)
        overlay = kwargs.get("overlay", False)
        ytarget = kwargs.get("ytarget", None)
        ytalign = kwargs.get("ytalign", "center")
        ysalign = kwargs.get("ysalign", "center")
        xtarget = kwargs.get("xtarget", None)
        xtalign = kwargs.get("xtalign", "center")
        xsalign = kwargs.get("xsalign", "center")
        height = kwargs.get("height", 'top')

        if name is None:
            name = 'box#{}'.format(len(self.objectlist))

        new = Box(
            self,
            name=name,
            pos=pos,
            size=size,
            dchar=dchar,
            splash=splash,
            overlay=overlay,
            ytarget=ytarget,
            ytalign=ytalign,
            ysalign=ysalign,
            xtarget=xtarget,
            xtalign=xtalign,
            xsalign=xsalign)

        self.place_object(new, height)
        return new

    def makedbox(self, **kwargs):
        """Make New Dynamic Box and place it in the object list.

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
            **height (str): height of object in objectlist, used for overlaps.

        Returns:
            DBox: New Dynamic Box.

        """

        name = kwargs.get("name", None)
        pos = kwargs.get("pos", (0, 0))
        size = kwargs.get("size", (1, 1))
        points = kwargs.get("points", None)
        style = kwargs.get("style", 'default')
        fg = kwargs.get('fg', 'default')
        bg = kwargs.get('bg', 'default')
        defaultpoints = kwargs.get("defaultpoints", False)
        overlay = kwargs.get("overlay", False)
        ytarget = kwargs.get("ytarget", None)
        ytalign = kwargs.get("ytalign", "center")
        ysalign = kwargs.get("ysalign", "center")
        xtarget = kwargs.get("xtarget", None)
        xtalign = kwargs.get("xtalign", "center")
        xsalign = kwargs.get("xsalign", "center")
        height = kwargs.get("height", 'top')

        if name is None:
            name = 'dbox#{}'.format(len(self.objectlist))

        new = DBox(self,
                   name=name,
                   pos=pos,
                   size=size,
                   points=points,
                   style=style,
                   fg=fg,
                   bg=bg,
                   overlay=overlay,
                   defaultpoints=defaultpoints,
                   ytarget=ytarget,
                   ytalign=ytalign,
                   ysalign=ysalign,
                   xtarget=xtarget,
                   xtalign=xtalign,
                   xsalign=xsalign)

        self.place_object(new, height)
        return new

    def maketbox(self, **kwargs):
        """Make new Text Box and place it in the object list.

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
            **justify (str): Text justification. Defaults to None.
            **ytarget (Box): vertical alignment target (can be compositor).
                Defaults to None.
            **ytalign (str): type of alignment to target vertically
            **ysalign (str): type of alignment to self vertically
            **xtarget (Box) horizontal alignment target (can be compositor).
                Defaults to None.
            **xtalign (str): type of alignment to target horizontally
            **xsalign (str): type of alignment to self horizontally
            **height (str): height of object in objectlist, used for overlaps.

        Returns:
            DBox: New Dynamic Box.

        """
        name = kwargs.get("name", None)
        pos = kwargs.get("pos", (0, 0))
        size = kwargs.get("size", (1, 1))
        style = kwargs.get("style", 'default')
        fg = kwargs.get('fg', 'default')
        bg = kwargs.get('bg', 'default')
        text = kwargs.get("text", '')
        wrap = kwargs.get("wrap", False)
        justify = kwargs.get("justify", None)
        border = kwargs.get("border", False)
        overlay = kwargs.get("overlay", False)
        ytarget = kwargs.get("ytarget", None)
        ytalign = kwargs.get("ytalign", "center")
        ysalign = kwargs.get("ysalign", "center")
        xtarget = kwargs.get("xtarget", None)
        xtalign = kwargs.get("xtalign", "center")
        xsalign = kwargs.get("xsalign", "center")
        height = kwargs.get("height", 'top')

        if name is None:
            name = 'tbox#{}'.format(len(self.objectlist))

        new = TBox(self,
                   name=name,
                   pos=pos,
                   size=size,
                   style=style,
                   fg=fg,
                   bg=bg,
                   text=text,
                   wrap=wrap,
                   justify=justify,
                   border=border,
                   overlay=overlay,
                   ytarget=ytarget,
                   ytalign=ytalign,
                   ysalign=ysalign,
                   xtarget=xtarget,
                   xtalign=xtalign,
                   xsalign=xsalign)

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
