"""Text Box.

Options for stripping newlines from input, as well as wrapping and box
outline.

"""

import textwrap
from .dbox import DBox


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
            **justify (str): Text justification. Defaults to None.
            **ytarget (Box): vertical alignment target (can be compositor).
                Defaults to None.
            **ytalign (str): type of alignment to target vertically
            **ysalign (str): type of alignment to self vertically
            **xtarget (Box) horizontal alignment target (can be compositor).
                Defaults to None.
            **xtalign (str): type of alignment to target horizontally
            **xsalign (str): type of alignment to self horizontally

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
        justify = kwargs.get('justify', None)
        # check arguments are valid
        if not isinstance(strip_newlines, bool):
            raise TypeError("strip_newlines is not bool")
        if not isinstance(wrap, bool):
            raise TypeError("wrap is not bool")
        super().__init__(
            parent=parent,
            name=name,
            pos=pos,
            size=size,
            overlay=overlay,
            fg=fg,
            bg=bg)

        self._text = text
        self.wrap = wrap
        self.justify = justify
        self.strip_newlines = strip_newlines

        self.setborder(border)
        self.update()

    @property
    def text(self):
        """Get the current text. Set a new text.

        Can be given a method to call to get text.

        Args:
            text (object): Any object with a __str__ method.

        """
        if callable(self._text):
            return self._text()
        return self._text

    @text.setter
    def text(self, text):
        self.text = text
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
        if border is not False and (
                border not in self.styles.keys()
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
                # changed this from -2 because it didn't seem necessary
                # justify below also follows changed state
                wrapper = textwrap.TextWrapper(width=self.size[1])
                wrapped = wrapper.wrap(text)

        else:
            wrapped = [text]

        # new, justify text
        if self.justify is not None:
            delta = 2 if self.border is not False else 0
            if self.justify == "left":
                wrapped = map(lambda s: s.ljust(self.size[1] - delta), wrapped)
            elif self.justify == "right":
                wrapped = map(lambda s: s.rjust(self.size[1] - delta), wrapped)
            elif self.justify == "center":
                wrapped = map(lambda s: s.center(
                    self.size[1] - delta), wrapped)

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
