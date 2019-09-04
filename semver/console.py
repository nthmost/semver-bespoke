"Supplies the 'semver' command line tool as defined in setup.py (entry_points)."

import fileinput

from .semver import SemverThing, NotSemanticVersion

def main():
    """Command line tool "semver" that compares a list of paired semantic version strings.

    Semver takes either piped input or a filename.  If it's a filename,
    the file is read line by line. Either way, each line is fed into a parsing loop that
    checks for 2 semantic version tags and attempts to compare them.  

    If the first is "older" than the second, the output for this line will be "before".  
    If the second is older than the first, the output for this line will be "after".  
    If they are equivalent, the output will be "equal".  

    Invalid lines are any that fail to parse as Semantic Version strings, or contain more 
    than 2 strings, or contain only 1 string.  Output will be "invalid" for these lines.

    Whitespace lines are ignored.
    """

    # The fileinput.input() function either takes piped input, or looks for a filename
    # and tries to open it and read it line by line.
    for line in fileinput.input():
        print()
        print(line.strip())
        words = line.strip().split()

        # blank line: skip it silently
        if len(words)==0:
            continue
        
        # too many or not enough items on this line: invalid
        if len(words) > 2 or len(words) == 1:
            print('invalid')
            continue

        # now we have 2 words to compare.
        try:
            sv1 = SemverThing(words[0])
            sv2 = SemverThing(words[1])
        except NotSemanticVersion:
            print('invalid')
            continue

        if sv1 < sv2:
            print('before')
        elif sv1 > sv2:
            print('after')
        elif sv1 == sv2:
            print('equal')


