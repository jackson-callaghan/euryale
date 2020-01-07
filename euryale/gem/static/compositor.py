"""Static Compositor and associated Boxtypes.

Box-based compositor with no animations or interactive elements. Absolutely
the most bare-bones system, really used as the skeleton for Dynamic Compositor
(dynamic.py).

TODO: parent assignment
TODO: parent-based alignment
TODO: alignment against target
TODO: Text justification
TODO: Box justification

TODO: expand Chars list
TODO: diagonal corners for DBox
TODO: EBox: edge-defined DBox (allows for multiple styles per edge,
                               matched corners)
TODO: ETBox: edge-defined TBox
"""

import os
import sys
from segment import Segment
from box import Box
from dbox import DBox
from tbox import TBox

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

    def makebox(
            self,
            name,
            pos=(0, 0),
            size=(0, 0),
            dchar=' ',
            splash=None,
            fg='default',
            bg='default',
            overlay=False,
            height='top'):
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

    def makedbox(
            self,
            name,
            pos=(0, 0),
            size=(0, 0),
            points=None,
            style='default',
            fg='default',
            bg='default',
            overlay=False,
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

        new = DBox(self,
                   name=name,
                   pos=pos,
                   size=size,
                   points=points,
                   style=style,
                   fg=fg,
                   bg=bg,
                   overlay=overlay)

        self.place_object(new, height)
        return new

    def maketbox(self,
                 name,
                 pos=(0, 0),
                 size=(0, 0),
                 points=None,
                 style='default',
                 fg='default',
                 bg='default',
                 overlay=False,
                 text='',
                 wrap=False,
                 border=False,
                 height='top'):
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

        new = TBox(self,
                   name=name,
                   pos=pos,
                   size=size,
                   points=points,
                   style=style,
                   fg=fg,
                   bg=bg,
                   text=text,
                   wrap=wrap,
                   border=border,
                   overlay=overlay)

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
