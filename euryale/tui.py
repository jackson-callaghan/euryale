"""

TODO: finish resize handling: add resize methods where applicable.
Inlcude defaultpoints argument for a dbox resize.
"""


from core import Character, utilities
import gem.static as gs
import os
import string


def main():
    termsize = get_terminal_size(fallback=(120, 29))
    size = (termsize[1] - 2, termsize[0])

    name = namelookup()
    os.system('cls' if os.name == 'nt' else 'clear')

    c = Character(utilities.read_char(name))

    g = gs.Compositor(size=size)
    details = g.makedbox(
        name='details',
        pos=(0, 0),
        size=(5, size[1]),
        defaultpoints=True
    )

    name = g.maketbox(
        name="name",
        size=(1, len(c.name)),
        text=c.name,
        fg="black",
        bg="white",
        ytarget=details,
        ytalign="top",
        ysalign="center",
        xtarget=details,
        xtalign="ileft",
        xsalign="aleft"
    )

    d_line1 = g.maketbox(
        name='line1',
        pos=(0, 0),
        size=(1, size[1] - 2),
        ytarget=details,
        ytalign="top",
        ysalign="below",
        xtarget=details,
        xtalign="ileft",
        xsalign="aleft"
    )
    d_line2 = g.maketbox(
        name='line1',
        size=(1, size[1] - 2),
        ytarget=d_line1,
        ytalign="bottom",
        ysalign="below",
        xtarget=d_line1,
        xtalign="left",
        xsalign="aleft"
    )

    g.composite()

    while True:

        # check if terminal is resized and resize everything
        ntermsize = get_terminal_size(fallback=(120, 29))
        if ntermsize != termsize:
            termsize = ntermsize
            size = (termsize[1] - 2, termsize[0])
            g.resize(size)  # don't make this one smaller than anything else
            details.resize((5, size[1]), True, True)
            d_line1.resize((1, size[1] - 2))
            d_line2.resize((1, size[1] - 2))

        if c.name != name.text:
            name.resize((1, len(c.name)))
            name.text = c.name

        d_line1.text = "Level {} {} {} {} | Size: {} | Alignment: {} | Religion: {}".format(
            string.capwords(str(c.character_level)),
            string.capwords(str(c.gender)),
            string.capwords(str(c.subrace)),
            string.capwords(str(c.race)),
            string.capwords(str(c.size)),
            string.capwords(str(c.alignment)),
            string.capwords(str(c.religion)),
        )
        d_line2.text = "Age: {} | Height: {} | Weight: {} | Skin: {} | Eyes: {} | Hair: {}".format(

            string.capwords(str(c.age)),
            c.height,
            c.weight,
            string.capwords(str(c.skin)),
            string.capwords(str(c.eyes)),
            string.capwords(str(c.hair))
        )

        g.composite()

        again = input("> ")
        try:  # made this shitty thing for live testing
            exec(again)
        except SyntaxError:
            continue


def namelookup(keyword=None):

    names = [f[0:-5] for f in os.listdir("data/characters")]
    if len(names) == 0:
        print("Warning: No character files found.".center(TERM_SIZE[0] - 1))

    if keyword is not None:
        names = [f for f in names if keyword.lower() in f.lower()]
        if len(names) == 0:
            return None

    print("=" * (TERM_SIZE[0] - 1))
    print("Found {} existing file{}".format(
        len(names),
        "s" if len(names) > 1 else ""
    ).center(TERM_SIZE[0] - 1))

    for i in range(len(names)):
        print("[{}] {}".format(i + 1, names[i]))

    print("=" * (TERM_SIZE[0] - 1))

    selector = input(
        "Select name by number or refine matches by keyword: \n> ")
    try:
        selector = int(selector)
        return names[selector - 1]
    except ValueError:
        while True:
            keyword_lookup = namelookup(selector)
            if keyword_lookup is None:
                print(
                    "No matches found. Please try a different keyword, or select from previous list.")
                selector = input("> ")
                try:
                    selector = int(selector)
                    return names[selector - 1]
                except ValueError:
                    continue
            else:
                return keyword_lookup

    return names


# courtesy of Bernardas Ališauskas
def get_terminal_size(fallback=(80, 24)):
    for i in range(0, 3):
        try:
            columns, rows = os.get_terminal_size(i)
        except OSError:
            continue
        break
    else:  # set default if the loop completes which means all failed
        columns, rows = fallback
    return columns, rows


TERM_SIZE = get_terminal_size(fallback=(120, 29))

if __name__ == "__main__":
    main()
