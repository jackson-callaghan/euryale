"""Test static."""

import static
from static import Compositor, Fore, Back, Style
import time


def standardtest():
    """Run a test of classes and methods.

    Standard test of classes and methods by rendering things.

    """
    sp = [['o', 'o', 'o'],
          ['o', 'l', 'o'],
          ['o', 'o', 'o'],
          ]
    myc = Compositor()
    box = myc.makebox('first', pos=(3, 3), size=(10, 10), dchar='x')
    myc.composite()
    box.splash_area(sp, (5, 5), (2, 3))
    sbox = myc.makebox('tiny', pos=(3, 15), size=(1, 1), dchar='s')
    myc.composite()
    sbox.setarea((0, 0), (0, 0), 'u')
    box.rectangle((0, 0), (2, 2), 'f')
    myc.composite()
    myc.removeobject('tiny')
    obox = myc.makebox('overlay', pos=(0, 0), size=(6, 6), overlay=True)
    obox.rectangle((0, 0), (5, 5), 'r', stroke=1, fg=Fore.RED)
    dbox = myc.makedbox('dynamic', (3, 40), (9, 9), overlay=True, bg='red')
    dbox.addpoints((0,  0), (8, 8), (0, 8), (8, 0))
    myc.composite()
    dbox.addpoints((0, 4), (8, 4))
    myc.composite()
    dbox.addpoints((4, 0), (4, 4), (4, 8))
    dbox.configure((7, 7), style='double', fg='green')
    myc.composite()
    dbox.configure(style='singleround')
    myc.composite()
    obox = myc.makedbox('test1', pos=(3, 55), size=(5, 5), overlay=True,
                        fg='blue',
                        style='dash2heavy',
                        points=[(0, 0), (4, 4), (4, 0), (2, 4)])
    myc.composite()
    tbox = myc.maketbox('tbox', (8, 3), (5, 50), wrap=True,
                        border=Style.SINGLEHEAVY,
                        overlay=False, fg='yellow',
                        text="Quis ea nulla quis reprehenderit sint fugiat \
    esse sit consectetur. Consectetur sint sunt adipisicing ipsum enim cupidat\
    est.Culpa laborum voluptate commodo incididunt et. ")

    myc.composite()
    tbox.settext("""Quis ea nulla quis reprehenderit sint fu
    esse sit consectetur. Consectetur sint sunt adipisicing ipsum enim cupidata
    est.Culpa laborum voluptate commodo incididunt et. """)
    myc.composite()
    tbox.setstyle(Style.BLOCKSHADEM)
    cbox = myc.makebox('colorbox',
                       pos=(5, 5),
                       size=(5, 5),
                       dchar=' ',
                       bg='white')
    myc.composite()


    time.sleep(5)


standardtest()
