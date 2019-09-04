from docopt import docopt
import sys

__version__ = '1.0.0'
__doc__ = """semver

Send standard input to this program.

Usage:
    semver 

Options:
   --help, -h       Show this screen.
   --version, -v    Show version of this CLI app.

"""


def main():

    args = docopt(__doc__, __version__)
    print(args)

    for line in sys.stdin.readlines():
        print(line)

