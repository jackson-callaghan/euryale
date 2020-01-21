"""

TODO: rework core.abilties to have generalized getters for abilities
This will allow the definitition of new ability maps which can immediately
fall into place with support for the upcoming modifier system.

"""


from core import Character, utilities
import gem.static as gs
import os
import string


class Main:

    def __init__(self):

        self.nan = None

        # honestly just define blank values for every self value you're
        # going to define later so it's not a pain

    def main(self):

        termsize = self.get_terminal_size(fallback=(120, 29))
        self.size = (termsize[1] - 2, termsize[0])

        self.name = self.namelookup()
        os.system('cls' if os.name == 'nt' else 'clear')

        self.c = Character(utilities.read_char(self.name))

        self.g = gs.Compositor(size=self.size)

        self.details = self.g.maketbox(
            name='details',
            pos=(0, 0),
            size=(5, self.size[1]),
            border='default'
        )

        self.name = self.g.maketbox(
            name="name",
            size=(1, len(self.c.name)),
            text=self.c.name,
            fg="black",
            bg="white",
            ytarget=self.details,
            ytalign="top",
            ysalign="center",
            xtarget=self.details,
            xtalign="ileft",
            xsalign="aleft"
        )

        self.ab_containers = []
        self.ab_names = []
        self.ab_box_size = (
            max([len(ab) for ab in self.c.ability_map.values()]) + 4,
            max([max([len(a) for a in ab])
                 for ab in self.c.ability_map.values()]) + 10
        )

        self.make_ab_containers()

        self.fill_ab_containers()

        self.g.composite()

        while True:

            # check if terminal is resized and resize everything
            ntermsize = self.get_terminal_size(fallback=(120, 29))
            if ntermsize != termsize:

                termsize = ntermsize
                size = (termsize[1] - 2, termsize[0])

                # resize compositor
                # don't make this one smaller than anything else
                self.g.resize(size)

                # resize details
                self.details.resize((5, size[1]))
                self.name.resize((1,
                                  len(self.c.name) if
                                  len(self.c.name) <= size[1] - 2 else
                                  size[1] - 2
                                  ))

                # resize skill boxes
                self.resize_ab_containers()

            if self.c.name != self.name.text:
                self.name.resize((1,
                                  len(self.c.name) if
                                  len(self.c.name) <= size[1] - 2 else
                                  size[1] - 2
                                  ))
                self.name.text = self.c.name

            if len(self.ab_containers) != len(self.c.ability_map):
                self.make_ab_containers()

            self.details.text = "Level {} {} {} {} | Size: {} | Alignment: {} | Religion: {}\nAge: {} | Height: {} | Weight: {} | Skin: {} | Eyes: {} | Hair: {}".format(
                string.capwords(str(self.c.character_level)),
                string.capwords(str(self.c.gender)),
                string.capwords(str(self.c.subrace)),
                string.capwords(str(self.c.race)),
                string.capwords(str(self.c.size)),
                string.capwords(str(self.c.alignment)),
                string.capwords(str(self.c.religion)),
                string.capwords(str(self.c.age)),
                self.c.height,
                self.c.weight,
                string.capwords(str(self.c.skin)),
                string.capwords(str(self.c.eyes)),
                string.capwords(str(self.c.hair))
            )

            self.fill_ab_containers()

            self.g.composite()

            again = input("> ")
            try:  # made this shitty thing for live testing
                exec(again)
            except SyntaxError:
                continue

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
                keyword_lookup = self.namelookup(selector)
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

    def make_ab_containers(self):
        self.ab_containers = []
        row = 0
        rowsize = 0
        y = 0
        n = 0
        for i, skill in enumerate(self.c.ability_map.keys()):
            if i == 0:
                self.ab_containers.append(self.g.maketbox(
                    pos=(0, 0),
                    name=skill,
                    size=self.ab_box_size,
                    border="default",
                    ytarget=self.details,
                    ytalign="bottom",
                    ysalign="below",
                    xtarget=self.details,
                    xtalign="left",
                    xsalign="aleft"
                ))
            elif y != row:
                self.ab_containers.append(self.g.maketbox(
                    pos=(0, 0),
                    name=skill,
                    size=self.ab_box_size,
                    border="default",
                    ytarget=self.ab_containers[i - n],
                    ytalign="bottom",
                    ysalign="below",
                    xtarget=self.ab_containers[i - n],
                    xtalign="left",
                    xsalign="aleft"
                ))
                row = y
                rowsize = 0
                n = 0
            else:
                self.ab_containers.append(self.g.maketbox(
                    pos=(0, 0),
                    name=skill,
                    size=self.ab_box_size,
                    border="default",
                    ytarget=self.ab_containers[i - 1],
                    ytalign="top",
                    ysalign="top",
                    xtarget=self.ab_containers[i - 1],
                    xtalign="oright",
                    xsalign="aleft"
                ))
            rowsize += self.ab_box_size[1]
            if rowsize + self.ab_box_size[1] >= self.size[1]:
                y += 1
            n += 1

            self.ab_names.append(self.g.maketbox(
                name="{} title".format(skill[0:3]),
                pos=(0, 0),
                size=(1, 3),
                text=skill[0:3].upper(),
                bg="white",
                fg="black",
                ytarget=self.ab_containers[i],
                ytalign="top",
                ysalign="center",
                xtarget=self.ab_containers[i],
                xtalign="ileft",
                xsalign="aleft"
            ))

    def fill_ab_containers(self):
        for ab in self.ab_containers:

            ab_mod = self.c.abilities.modifiers[ab.name]
            if ab_mod >= 0:
                ab_mod = "+{}".format(ab_mod)
            else:
                ab_mod = "-{}".format(ab_mod)
            sk_info = " {:>2} Score\n{}{:>2} Modifier\n".format(
                self.c.abilities.abilities[ab.name],
                ab_mod[0],
                ab_mod[1:]
            )
            for sk in self.c.ability_map[ab.name]:
                prof = self.c.abilities.has_proficiency(sk)
                if prof == 2:
                    prof = "^"
                elif prof == 1:
                    prof = "*"
                else:
                    prof = " "
                sk_mod = self.c.abilities.skill_mod(sk)
                if sk_mod >= 0:
                    sk_mod = "+{}".format(sk_mod)
                else:
                    sk_mod = "-{}".format(sk_mod)
                sk_info += "{}{:>2} [{}] {}\n".format(
                    sk_mod[0], sk_mod[1:], prof, string.capwords(sk))
            ab.text = sk_info

    def resize_ab_containers(self):
        row = 0
        rowsize = 0
        y = 0
        n = 0
        for i, box in enumerate(self.ab_containers):
            if i == 0:
                box.ytarget = self.details
                box.ytalign = "bottom"
                box.ysalign = "below"
                box.xtarget = self.details
                box.xtalign = "left"
                box.xsalign = "aleft"
            elif y != row:
                box.ytarget = self.ab_containers[i - n]
                box.ytalign = "bottom"
                box.ysalign = "below"
                box.xtarget = self.ab_containers[i - n]
                box.xtalign = "left"
                box.xsalign = "aleft"
                row = y
                rowsize = 0
                n = 0
            else:
                box.ytarget = self.ab_containers[i - 1]
                box.ytalign = "top"
                box.ysalign = "top"
                box.xtarget = self.ab_containers[i - 1]
                box.xtalign = "oright"
                box.xsalign = "aleft"
            rowsize += self.ab_box_size[1]
            if rowsize + self.ab_box_size[1] >= self.size[1]:
                y += 1
            n += 1


if __name__ == "__main__":
    main = Main()
    main.main()
