from core.character import Character
from core.utilities import read_char


def test():
    tanya = Character(read_char("Tanya Degurechaff"))
    print(tanya)
    return tanya


if __name__ == "__main__":
    test()
