"""Contains the primary engine of Semver parsing, SemverThing.  Supplies NotSemanticVersion exception.
"""

import re

# regular expression for parsing semantic version text as per semver 2.0 documentation
re_semver = re.compile('^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')

# regular expression helpful for breaking 2 prerelease strings into symmetric parts.
re_prerelease = re.compile('^(?P<abc>[a-zA-Z]*)(?P<num>([-.\d]*)?)')

class NotSemanticVersion(Exception):
    "Raised when supplied string fails to parse into semantic version information during parse_semver_text."
    pass


def parse_semver_text(text):
    """Uses regular expression to parse out the components of a semantic version string.
    
    If regular expression parsing fails, raises NotSemanticVersion exception.

    The dictionary returned should contain the following keys if successful:

        major
        minor
        patch
        prerelease
        buildmetadata

    :param text: (str)
    :return: match group from regular expression (if successful)
    :rtype: dict
    :raises: NotSemanticVersion
    """
    res = re_semver.match(text)
    if not res:
        raise NotSemanticVersion('Supplied text "{}" did not pass regular expression parsing.'.format(text))
    return res.groupdict()


def rec_cmp_releases(one, two):
    """Recursive function that compares two version strings represented as lists
    to determine which one comes "after" / takes precedence, or if they are equivalent.

    List items must be integers (will throw TypeError otherwise).

    If the left argument ("one") is a later version, returns 1.
    If the right argument ("two") is a later version, returns 2.
    If they are equivalent, returns 0.

    :param one: list of ints to compare to two
    :param two: list of ints to compare to one
    :returns: code in (0, 1, 2)
    :rtype: int
    """
    # we've exhausted all three levels of comparison, so logically we're at equivalence.
    if len(one)==0:
        return 0

    top1 = one[0]
    top2 = two[0]

    if top1 > top2:
        return 1
    elif top1 < top2:
        return 2
    else:
        return rec_cmp_releases(one[1:], two[1:])


def rec_cmp_prereleases(one, two):
    """Recursive function that compares two version strings represented as lists
    to determine which takes precedence.  If it is the left argument ("one"), the 
    result will be a 1.  If the righthand argument wins ("two"), the result will be
    a 2.  If the two are equivalent (i.e. are the same string), the result is a 0.

    :param one: left-hand version str
    :param two: right-hand version str
    :return: 0, 1, or 2
    :rtype: int
    """
    if one == two:
        return 0

    # if either has reached its zenith of productivity, the other has won.
    #
    # (Note that this is only correct in the context of there being conditionals in
    #  the cmp_prerelease function that already handle the case in which one 
    #  version string has a prerelease and the other one doesn't!  This recursive
    #  comparator function won't ever be invoked in that situation.) 
    if len(one) == 0:
        return 2
    elif len(two) == 0:
        return 1

    # ok so we still have two values to compare.
    # try to make ints; if we fail, then we have ASCII.
    cmp_strs = {}
    cmp_ints = {}
    try:
        cmp_ints[1] = int(one[0])
    except ValueError:
        cmp_strs[1] = one[0]

    try:
        cmp_ints[2] = int(two[0])
    except ValueError:
        cmp_strs[2] = two[0]

    if len(cmp_strs)==2:
        # if the two strings are equivalent, recurse down further.
        # if not, declare a winner by ASCII value.
        if cmp_strs[1] == cmp_strs[2]:
            return rec_cmp_prereleases(one[1:], two[1:])
        elif cmp_strs[1] > cmp_strs[2]:
            return 1
        elif cmp_strs[1] < cmp_strs[2]:
            return 2

    elif len(cmp_ints)==2:
        # if the two integers are equivalent, recurse down further.
        # otherwise, declare a winner by integer value. 
        if cmp_ints[1] == cmp_ints[2]:
            return rec_cmp_prereleases(one[1:], two[1:])
        elif cmp_ints[1] > cmp_ints[2]:
            return 1
        elif cmp_ints[1] < cmp_ints[2]:
            return 2

    # Apples and oranges: ASCII always wins.
    return list(cmp_strs.keys())[0]


def cmp_prerelease(sv1, sv2):
    """Helper function for comparing the prerelease strings on two SemverThing objects.

    Note that if one SV object has NO prerelease string and the other does, the first one with
    the empty string takes precedence.
    
    if sv1 has precedence over sv2, returns the number 1.
    if sv2 has precedence over sv1, returns the number 2.
    if they are equivalent, returns the number 0.
    """
    if sv1.prerelease == sv2.prerelease:
        return 0

    if sv1.prerelease and sv2.prerelease:
        # If we have something like alpha-11 and alpha-2, we want to compare the number field 
        # as numbers (not ASCII, which would give the wrong answer for that pair).
        #
        # Another possiblity is that we're just comparing numbers, e.g. "1-2-3" to "1-2-4"
        # 
        # In any case, let's standardize to using dots instead of dashes.
        pre1 = sv1.prerelease.replace('-', '.')
        pre2 = sv2.prerelease.replace('-', '.')

        # convert each to a list and then recursively compare the successive strings to each other.
        return rec_cmp_prereleases(pre1.split('.'), pre2.split('.'))
                    
    # if sv1 has a prerelease, and sv2 doesn't, sv2 takes precedence
    elif sv1.prerelease and not sv2.prerelease:
        return 2

    # finally, if sv2 has a prerelease and sv1 doesn't, sv1 takes precedence. 
    return 1


class SemverThing(object):
    """ You can build a SemverThing in three ways:

    1) Instantiate with a plain string, e.g. "1.2.3".  The text variable will be parsed
       through regular expressions to identify each part of the semver construction. For example:

           sv = SemverThing("1.2.3-prerelease+build")
           print(sv.build)       # build
           print(sv.major)       # 1
           print(sv.prerelease)  # prerelease
           print(sv.minor)       # 2
           print(sv.patch)       # 3

    2) Instantiate with keyword arguments, for example:
  
           sv = SemverThing(major=1, minor=2, patch=3)  #, prerelease, buildmetadata 

    3) Instantiate without arguments to create a blank slate, to which you can
       assign values to its version attributes one at a time.  
       For Example:

           sv = SemverThing()
           sv.major = 1
           sv.minor = 2
           sv.patch = 3 
           print(sv)              # 1.2.3

           sv.buildmetadata = "somebuild"
           print(sv)              # 1.2.3+somebuild

           sv.prerelease = "alpha"
           print(sv)              # 1.2.3-alpha+somebuild


    Usage:

        All arithmetic comparison operators are implemented on this object, so you can do:

           sv1 = SemverThing('1.2.3-alpha')
           sv2 = SemverThing('1.2.3')

           print(sv1 > sv2)      # False
           print(sv1 != sv2)     # True
           print(sv2 > sv1)      # True


        NOTE that numerical version components (major, minor, patch) are converted to integers within
        the object for ease of comparison.

        To convert a SemverThing to a composed version string, simply use the python str operator::

            print(sv1)                               # "1.2.3-alpha"
            print("My version is %s" % sv2)          # "My version is 1.2.3"

    """

    def __init__(self, text=None, **kwargs):
        """ text argument overrides use of kwargs. """

        if text: 
            try:
                kwargs = parse_semver_text(text)
            except TypeError:
                # attempt to create SemverThing using number or other nonsense.
                raise NotSemanticVersion('{} is not a valid string.'.format(text))

        self.major = kwargs.get('major', None)
        self.minor = kwargs.get('minor', None)
        self.patch = kwargs.get('patch', None)
        self.prerelease = kwargs.get('prerelease', '')
        self.buildmetadata = kwargs.get('buildmetadata', '')

    # MAGIC PROPERTIES for the numerical attributes:
    #   1) convert input to integer (raise ValueError if not convertible to int)
    #   2) allow setting properties to None without error.

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, value):
        if value is None:
            self._major = None
            return
        self._major = int(value)

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, value):
        if value is None:
            self._minor = None 
            return 
        self._minor = int(value)

    @property
    def patch(self):
        return self._patch

    @patch.setter
    def patch(self, value):
        if value is None:
            self._patch = None
            return
        self._patch = int(value)


    # COMPARISON OPERATOR DEFINTIIONS: 
    #           The left-hand object in the statement is "self"; the right-hand is "other".
    #           In cmp_* functions these map to one (1) and two (2) respectively.

    # <
    def __lt__(self, other):
        conditions = {0: False,
                      1: False,
                      2: True
                     }

        result = rec_cmp_releases([self.major, self.minor, self.patch],
                                  [other.major, other.minor, other.patch])

        if result in (1,2): 
            return conditions[result]

        # equivalence? drill down into prerelease.
        return conditions[cmp_prerelease(self, other)]

    # <=
    def __le__(self, other):
        if self.__eq__(other):
            return True

        if self.__lt__(other):
            return True

        return False

    # >
    def __gt__(self, other):
        conditions = {0: False,
                      2: False,
                      1: True
                     }

        result = rec_cmp_releases([self.major, self.minor, self.patch],
                                  [other.major, other.minor, other.patch])

        if result in (1,2): 
            return conditions[result]

        # equivalence? drill down into prerelease.
        return conditions[cmp_prerelease(self, other)]

    # >=
    def __ge__(self, other):
        if self.__eq__(other):
            return True

        if self.__gt__(other):
            return True

        return False

    # ==
    def __eq__(self, other):
        conditions = {0: True,
                      1: False,
                      2: False,   
                     }

        # if the result is anything other than 0, these are not equivalent releases.
        if rec_cmp_releases([self.major, self.minor, self.patch],
                            [other.major, other.minor, other.patch]):
            return False

        # OK let's check the prereleases.
        return conditions[cmp_prerelease(self, other)]

    # !=
    def __ne__(self, other):
        return not(self.__eq__(other))

    # OBJECT REPRESENTATION FUNCTIONS: to_dict, to_list, __str__, __repr__

    def to_dict(self):
        "Returns a dictionary representation of the attributes on this object."
        return {'major': self.major,
                'minor': self.minor,
                'patch': self.patch,
                'prerelease': self.prerelease,
                'buildmetadata': self.buildmetadata,
               }

    def __str__(self):
        out = '{major}.{minor}.{patch}'
        if self.prerelease and self.buildmetadata:
            out += '-{prerelease}+{buildmetadata}'
        elif self.prerelease:
            out += '-{prerelease}'
        elif self.buildmetadata:
            out += '+{buildmetadata}'
        return out.format(**self.to_dict())

    def __repr__(self):
        return '<SemverThing {}>'.format(str(self))

