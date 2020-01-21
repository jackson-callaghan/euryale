"""

TODO: add documentation where necessary
TODO: redo anything that should be turned into a property (see box classes)
TODO: abilities and skills (ensure dynamic resizing)

"""


from core import Character, utilities
import gem.static as gs
import os
import string
import math
from gem.static.style import Chars


class Main:

    def __init__(self):

        self.nan = None

        # honestly just define blank values for every self value you're
        # going to define later so it's not a pain

    def namelookup(self, keyword=None):
        termsize = self.get_terminal_size(fallback=(120, 29))

        names = [f[0:-5] for f in os.listdir("data/characters")]

        if len(names) == 0:
            print("Warning: No character files found.".center(
                termsize[0] - 1))

        if keyword is not None:
            names = [f for f in names if keyword.lower() in f.lower()]
            if len(names) == 0:
                return None

        print("=" * (termsize[0] - 1))
        print("Found {} existing file{}".format(
            len(names),
            "s" if len(names) > 1 else ""
        ).center(termsize[0] - 1))

        for i in range(len(names)):
            print("[{}] {}".format(i + 1, names[i]))

        print("=" * (termsize[0] - 1))

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

    def main(self):

        termsize = self.get_terminal_size(fallback=(120, 29))
        size = (termsize[1] - 2, termsize[0])

        name = self.namelookup()
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

        skill_containers = []
        skill_names = []
        i = max([max([len(a) for a in ab])
                 for ab in c.ability_map.values()])
        skill_container_size = (
            max([len(ab) for ab in c.ability_map.values()]) + 4,
            max([max([len(a) for a in ab])
                 for ab in c.ability_map.values()]) + 10
        )

        row = 0
        rowsize = 0
        y = 0
        n = 0

        for i, skill in enumerate(c.ability_map.keys()):
            if i == 0:
                skill_containers.append(g.maketbox(
                    pos=(0, 0),
                    name=skill,
                    size=skill_container_size,
                    border="default",
                    ytarget=details,
                    ytalign="bottom",
                    ysalign="below",
                    xtarget=details,
                    xtalign="left",
                    xsalign="aleft"
                ))
            elif y != row:
                skill_containers.append(g.maketbox(
                    pos=(0, 0),
                    name=skill,
                    size=skill_container_size,
                    border="default",
                    ytarget=skill_containers[i - n],
                    ytalign="bottom",
                    ysalign="below",
                    xtarget=skill_containers[i - n],
                    xtalign="left",
                    xsalign="aleft"
                ))
                row = y
                rowsize = 0
            else:
                skill_containers.append(g.maketbox(
                    pos=(0, 0),
                    name=skill,
                    size=skill_container_size,
                    border="default",
                    ytarget=skill_containers[i - 1],
                    ytalign="top",
                    ysalign="top",
                    xtarget=skill_containers[i - 1],
                    xtalign="oright",
                    xsalign="aleft"
                ))
            rowsize += skill_container_size[1]
            if rowsize + skill_container_size[1] >= size[1]:
                y += 1
            n += 1

        for ab in skill_containers:
            skill_names.append(g.maketbox(
                name="{} title".format(ab.name),
                pos=(0, 0),
                size=(1, 3),
                text=ab.name[0:3].upper(),
                bg="white",
                fg="black",
                ytarget=ab,
                ytalign="top",
                ysalign="center",
                xtarget=ab,
                xtalign="ileft",
                xsalign="aleft"
            ))
            ab_mod = c.abilities.modifiers[ab.name]
            if ab_mod >= 0:
                ab_mod = "+{}".format(ab_mod)
            else:
                ab_mod = "-{}".format(ab_mod)
            sk_info = " {:>2} Score\n{}{:>2} Modifier\n".format(
                c.abilities.abilities[ab.name],
                ab_mod[0],
                ab_mod[1:]
            )
            for sk in c.ability_map[ab.name]:
                prof = c.abilities.has_proficiency(sk)
                if prof == 2:
                    prof = "^"
                elif prof == 1:
                    prof = "*"
                else:
                    prof = " "
                sk_mod = c.abilities.skill_mod(sk)
                if sk_mod >= 0:
                    sk_mod = "+{}".format(sk_mod)
                else:
                    sk_mod = "-{}".format(sk_mod)
                sk_info += "{}{:>2} [{}] {}\n".format(
                    sk_mod[0], sk_mod[1:], prof, string.capwords(sk))
            ab.text = sk_info

        g.composite()

        while True:

            # check if terminal is resized and resize everything
            ntermsize = self.get_terminal_size(fallback=(120, 29))
            if ntermsize != termsize:

                termsize = ntermsize
                size = (termsize[1] - 2, termsize[0])

                # resize compositor
                # don't make this one smaller than anything else
                g.resize(size)

                # resize details
                details.resize((5, size[1]), True, True)
                d_line1.resize((1, size[1] - 2))
                d_line2.resize((1, size[1] - 2))
                name.resize((1,
                             len(c.name) if
                             len(c.name) <= size[1] - 2 else size[1] - 2
                             ))

                row = 0
                rowsize = 0
                y = 0
                n = 0

                # resize skill boxes
                for i, box in enumerate(skill_containers):
                    if i == 0:
                        box.ytarget = details
                        box.ytalign = "bottom"
                        box.ysalign = "below"
                        box.xtarget = details
                        box.xtalign = "left"
                        box.xsalign = "aleft"
                    elif y != row:
                        box.ytarget = skill_containers[i - n]
                        box.ytalign = "bottom"
                        box.ysalign = "below"
                        box.xtarget = skill_containers[i - n]
                        box.xtalign = "left"
                        box.xsalign = "aleft"
                        row = y
                        rowsize = 0
                    else:
                        box.ytarget = skill_containers[i - 1]
                        box.ytalign = "top"
                        box.ysalign = "top"
                        box.xtarget = skill_containers[i - 1]
                        box.xtalign = "oright"
                        box.xsalign = "aleft"
                    rowsize += skill_container_size[1]
                    if rowsize + skill_container_size[1] >= size[1]:
                        y += 1
                    n += 1

            if c.name != name.text:
                name.resize((1,
                             len(c.name) if
                             len(c.name) <= size[1] - 2 else size[1] - 2
                             ))
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

    # courtesy of Bernardas Ališauskas

    def get_terminal_size(self, fallback=(80, 24)):
        for i in range(0, 3):
            try:
                columns, rows = os.get_terminal_size(i)
            except OSError:
                continue
            break
        else:  # set default if the loop completes which means all failed
            columns, rows = fallback
        return columns, rows


if __name__ == "__main__":
    main = Main()
    main.main()
