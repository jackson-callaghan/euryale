from static import Compositor, Fore, Back, Style, Chars
import time


myc = Compositor()

sizes = [
    # 1,
    # 2,
    # 3,
    4,
    # 5
]

for theight in sizes:
    for twidth in sizes:
        target = myc.makedbox(
            'dynamic',
            pos=(5, 5),
            size=(theight, twidth),
            overlay=False,
            bg='red')
        for mheight in sizes:
            for mwidth in sizes:
                mbox = myc.makedbox(
                    'move',
                    size=(mheight, mwidth),
                    overlay=True,
                    fg='green',
                    bg='blue'
                )

                for xt in mbox.xtalign_possible:
                    mbox.xtarget = target
                    mbox.xtalign = xt

                    for xs in mbox.xsalign_possible:
                        mbox.xsalign = xs
                        myc.composite()
                        cont = input("target size ({},{}); mbox size ({},{}); alignment types ({}, {})".format(
                            target.size[0],
                            target.size[1],
                            mbox.size[0],
                            mbox.size[1],
                            xt,
                            xs
                        ))
                myc.removeobject(mbox)
