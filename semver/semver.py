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

    :param text: (str)
    :return: 
    :rtype: dict
    :raises: NotSemanticVersion
    """
    
    res = re_semver.match(text)
    if not res:
        raise NotSemanticVersion
    
    print(res)
    return res



class SemverThing(object):
    """ You can build a SemverThing in three ways:

    1) Instantiate with a plain string, e.g. "1.2.3".  The text variable will be parsed
       through regular expressions to identify each part of the semver construction.

    2) Instantiate with keyword arguments, for example:
  
       sv = SemverThing(major=1, minor=2, patch=3)  #, pre-release, and metadata 
       print(sv)

    3) Instantiate without arguments to create a blank slate, to which you can
       assign values to its version attributes one at a time.  For Example:

       sv = SemverThing()
       sv.major = 1
       sv.minor = 2
       sv.patch = 3 
    """

    def __init__(self, text=None, **kwargs):
        """ text argument overrides use of kwargs. """

        if text: 
            kwargs = parse_semver_text(text)

        self.major = kwargs.get('major', None)
        self.minor = kwargs.get('minor', None)
        self.patch = kwargs.get('patch', None)
        self.prerelease = kwargs.get('prerelease', None)
        self.metadata = kwargs.get('metadata', None)

    def to_dict(self):
        return {'major': self.major,
                'minor': self.minor,
                'patch': self.patch,
                'prerelease': self.prerelease,
                'metadata': self.metadata,
               }

    def __str__(self):
        out = '{major}.{minor}.{patch}'
        if self.prerelease:
            out += '.{prerelease}'
        return out.format(self.to_dict())



