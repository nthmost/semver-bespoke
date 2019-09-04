"""Contains the primary engine of Semver parsing, $NAME_OF_OBJECT"""
import re

# regular expression for parsing semantic version text as per semver 2.0 documentation
re_semver = re.compile('^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')

class NotSemanticVersion(Exception):
    "Raised when supplied string fails to break into semantic version information during parse_semver_text."
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
        raise NotSemanticVersion
    return res.groupdict()


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
        #TODO: string comparison to see if we want to compare numbers.

        if sv1.prerelease > sv2.prerelease:
            # e.g. "beta" > "alpha" --> True
            return 1
        elif sv1.prerelease < sv2.prerelease:
            # e.g.  "beta" < "gamma" --> True
            return 2

    elif sv1.prerelease and not sv2.prerelease:
        return 2

    # which leaves us with sv2 having a prerelease and sv1 not having one.
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
    #           the left-hand object in the statement is "self"; the right-hand is "other".
    #
    # <
    def __lt__(self, other):
        if self.major < other.major:
            return True

        if self.major == other.major:
            if self.minor < other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch < other.patch:
                    return True
                elif self.patch > other.patch:
                    return False
                else:
                    # patches are equivalent; compare on prerelease.
                    # here we only want to know if other > self (result of 2).
                    return True if cmp_prerelease(self, other) == 2 else False

        # self.major > self.minor
        return False

    # <=
    def __le__(self, other):
        if self.__eq__(other):
            return True

        if self.__lt__(other):
            return True

        return False

    # >
    def __gt__(self, other):
        if self.major > other.major:
            return True

        elif self.major == other.major:
            # majors are equivalent: compare on minor
            if self.minor > other.minor:
                return True

            elif self.minor == other.minor:
                # both minors are equal; compare on patch
                if self.patch > other.patch:
                    return True
                elif self.patch < other.patch:
                    return False 

                elif self.patch == other.patch:
                    # compare prereleases -- return is in (0, 1, 2) 
                    # here we only want to know if the result was 1 (self has precendence).
                    return True if cmp_prerelease(self, other) == 1 else False

        # self.major < self.minor
        return False

    # >=
    def __ge__(self, other):
        if self.__eq__(other):
            return True

        if self.__gt__(other):
            return True

        return False

    # ==
    def __eq__(self, other):
        if (self.major == other.major) and (self.minor == other.minor) and (self.patch == other.patch):
            # compare prerelease strings (pos results: 0, 1, 2 with 0 meaning equivalence).
            if cmp_prerelease(self, other) == 0:
                return True
        return False

    # !=
    def __ne__(self, other):
        return not(self.__eq__(other))

    # OBJECT REPRESENTATION FUNCTIONS: to_dict, __str__, __repr__

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

