"""

TODO: write getter methods for basically everything in character class
"""


from core import Character, utilities
import gem.static as gs
import os


def main():
    size = (TERM_SIZE[1] - 2, TERM_SIZE[0])

    name = namelookup()
    os.system('cls' if os.name == 'nt' else 'clear')

    c = Character(utilities.read_char(name))

    g = gs.Compositor(size=size)
    details = g.makebox(
        name='details',
        pos=(0, 0)
    )
    details.setarea(
        c1=(0, 0),
        c2=details.size,
        char=gs.style.Chars.BLOCK_FULL,
        fg="white"
    )
    name = g.maketbox(
        name="name",
        size=(1, len(c.name)),
        text=c.get_name,
        overlay=True,
        fg="black",
        ytarget=details,
        ytalign="top",
        ysalign="center",
        xtarget=details
    )

    g.composite()

    while True:
        c.name = "Tonka Dogchef"
        my_test = input("\n> ")
        g.composite()


def namelookup(keyword=None):

    names = [f[0:-5] for f in os.listdir("data/characters")]
    if len(names) == 0:
        print("Warning: No character files found.".center(TERM_SIZE[0] - 1))

    if keyword is not None:
        names = [f for f in names if keyword.lower() in f.lower()]
        if len(names) == 0:
            return None

    print("=" * (TERM_SIZE[0] - 1))
    print("Found {} existing files".format(
        len(names)).center(TERM_SIZE[0] - 1))

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
