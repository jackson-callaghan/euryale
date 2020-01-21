"""A small collection of classes with potentially useful common values.

While most of these are typically best used automatically via the classes, they
are also available here if need be.
"""


class Fore():
    """Foreground colors.

    Can use attributes as arguments or use the attribute name str in lowercase
    as arguments.

    """

    BLACK = '30'
    RED = '31'
    GREEN = '32'
    YELLOW = '33'
    BLUE = '34'
    MAGENTA = '35'
    CYAN = '36'
    WHITE = '37'
    RESET = '39'


class Back():
    """Background colors.

    Can use attributes as arguments or use the attribute name str in lowercase
    as arguments.

    """

    BLACK = '40'
    RED = '41'
    GREEN = '42'
    YELLOW = '43'
    BLUE = '44'
    MAGENTA = '45'
    CYAN = '46'
    WHITE = '47'
    RESET = '49'


class Style():
    """Style keys.

    Can use attributes as arguments or use the attribute name str in lowercase
    as arguments.

    """

    DEFAULT = "─│┌┐└┘├┤┬┴┼"
    SINGLELIGHT = "─│┌┐└┘├┤┬┴┼"
    SINGLEROUND = "─│╭╮╰╯├┤┬┴┼"
    SINGLEHEAVY = "━┃┏┓┗┛┣┫┳┻╋"
    DOUBLE = "═║╔╗╚╝╠╣╦╩╬"
    DASH2LIGHT = "╌╎┌┐└┘├┤┬┴┼"
    DASH2HEAVY = "╍╏┏┓┗┛┣┫┳┻╋"
    DASH3LIGHT = "┄┆┌┐└┘├┤┬┴┼"
    DASH4HEAVY = "┅┇┏┓┗┛┣┫┳┻╋"
    DASH4LIGHT = "┈┊┌┐└┘├┤┬┴┼"
    DASH4HEAVY = "┉┋┏┓┗┛┣┫┳┻╋"
    DASH2ROUND = "╌╎╭╮╰╯├┤┬┴┼"
    DASH3ROUND = "┄┆╭╮╰╯├┤┬┴┼"
    DASH4ROUND = "┈┊╭╮╰╯├┤┬┴┼"
    BLOCKSHADEL = "░░░░░░░░░░░"
    BLOCKSHADEM = "▒▒▒▒▒▒▒▒▒▒▒"
    BLOCKSHADED = "▓▓▓▓▓▓▓▓▓▓▓"
    FULLBLOCK = "███████████"


class Chars():
    """Commonly used characters.

    For accessing characters you might commonly use for whatever reason with
    greater ease than might be typical.
    """

    BLOCK_LIGHT = "░"
    BLOCK_MEDIUM = "▒"
    BLOCK_HEAVY = "▓"
    BLOCK_FULL = "█"
    CHECK_EMPTY = "☐"
    CHECK_CHECK = "☑"
    CHECK_X = "☒"
