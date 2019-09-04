"Supplies the 'semver' command line tool as defined in setup.py (entry_points)."

import fileinput

from .semver import SemverThing, NotSemanticVersion



def compare_versions(vstr1, vstr2):
    """This function compares two version strings and returns an answer as to whether
    the first in the pair is "before", "after" or "equal" to the second in the pair.

    If either string cannot be parsed as a semantic version string, the answer 
    returned will be "invalid".

    :param vstr1: version string (plain text)
    :param vstr2: version string (plain text, different from 1st)
    :return: answer (str)
    :rtype: str
    """
    try:
        sv1 = SemverThing(vstr1)
        sv2 = SemverThing(vstr2)
    except NotSemanticVersion:
        return 'invalid'

    try:
        if sv1 < sv2:
            return 'before'
        elif sv1 > sv2:
            return 'after'
        elif sv1 == sv2:
            return 'equal'
    except TypeError:
        # attempt to compare SemverThing in which one or more properties are None
        return 'invalid'


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
        #print()    #debug
        #print(line.strip())        #debug
        words = line.strip().split()

        # blank line: skip it silently
        if len(words)==0:
            continue
        
        # too many or not enough items on this line: invalid
        if len(words) > 2 or len(words) == 1:
            print('invalid')
            continue

        # now we should have 2 words to compare.
        print(compare_versions(words[0], words[1]))

