# semver-bespoke
Implementation of Semver 2.0 in Python by Naomi Most, 9/3/2019

The official Semver 2.0 reference can be found at https://semver.org/spec/v2.0.0.html

This project's primary product is the `semver` console script which is operated like so:

```
semver <input_filename>

echo "release pair\nrelease pair\n" >> semver
```

This tool takes pairs of semantic version strings, determines if they are valid, 
and then compares these pairs to determine (and print) their relationship to each other.

For example, the pair `2.3.4` and `2.3.5` would give the result "before", meaning that 2.3.4
came before 2.3.5.  The pair `1.3.5` and `1.3.1` would give the result "after".  Other possible
results are "equal" and "invalid".  Lines with only 1 or more than 2 words are treated as "invalid".

This package also provides a handy-dandy object for parsing and comparing semantic version strings.
It's called the SemverThing.  See Developer API section below for more.

## Setup ##

You can install globally by using pip, or you can install from the repo within a virtual environment.

Method 1: 

```
pip install -e git+https://github.com/nthmost/semver-bespoke/#egg=semver
```

This installs the `semver` console app on your system so it's accessible from anywhere.


Method 2:

Clone this repo.

After cloning this repo, navigate into the newly created folder and create a python
virtual environment for this project::

```
python3 -m venv
source venv/bin/activate
python setup.py install
```

If all went well, you should have the `semver` command-line tool at your disposal.

The `semver` CLI tool reads each line it is given and determines (prints) the relationship 
of the two semantic version tags (separated by any whitespace, 2 per line). 

To use it, you have two options.  You can pipe it lines of input via stdin...

```
echo "1.2.3  1.2.4" > semver
```

Or you can read from a file containing readable text.

```
semver input.txt
```

## Developer API ##

The real work of parsing and comparing versions is done on the SemverThing object.

Yes I realize this is a silly name.

Basic Usage:

```
from semver import SemverThing

sv1 = SemverThing('2.4.5-alpha')
sv2 = SemverThing('2.4.5-beta')

>>> print(sv1 > sv2)
False

>>> print(sv2 == sv1)
False

>>> print(sv2 > sv1)
True
```


You can build a SemverThing in three different ways:

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

    SemverThing Usage:

        All arithmetic comparison operators are implemented on this object, so you can do:

           sv1 = SemverThing('1.2.3-alpha')
           sv2 = SemverThing('1.2.3')

           print(sv1 > sv2)      # False
           print(sv1 != sv2)     # True
           print(sv2 > sv1)      # True


        NOTE that numerical version components (major, minor, patch) are converted to integers within
        the object for ease of comparison.

        To convert a SemverThing to a composed version string, simply use the python str operator:

            print(sv1)                               # "1.2.3-alpha"
            print("My version is %s" % sv2)          # "My version is 1.2.3"

        Finally, there's a convenience function `to_dict()` that converts the salient components of the
        class into values in a dictionary.  For example:

            print(sv1.to_dict())  # {'major': 1, 'minor': 2, 'patch': 3, 'prerelease': 'alpha', 'buildmetadata': ''}



## Testing ##

You can run the unit tests within the same virtual environment by using py.test in the root
of the repo:

```
py.test tests
```

The tests contain a lot of different fixtures of possible release strings, but most importantly,
there's a test that checks the Gold Standard Sequence of comparison set by the Semver Spec.
To wit:

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0
```


## Contact ##

You can contact the author (@nthmost) via GitHub, file an issue and/or submit a pull request at your leisure.

