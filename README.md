# semver-bespoke
Implementation of Semver 2.0 in Python by Naomi Most, 9/3/2019

The official Semver 2.0 reference can be found at https://semver.org/spec/v2.0.0.html

## Setup ##

After cloning this repo, navigate into the newly created folder and create a python
virtual environment for this project::

  pyvenv ve
  source ve/bin/activate
  python setup.py install

If all went well, you should have the `semver` command-line tool at your disposal.  You can either 
feed semver the name of a file containing readable text, or you can pipe it lines of input via stdin.

  echo "1.2.3  1.2.4" > semver

  semver input.txt


## Developer API ##

The real work of parsing and comparing versions is done on the SemverThing object.

Yes I realize this is a silly name.

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

        To convert a SemverThing to a composed version string, simply use the python str operator::

            print(sv1)                               # "1.2.3-alpha"
            print("My version is %s" % sv2)          # "My version is 1.2.3"


## Contact ##

This library and command line tool was written for a coding assignment by Naomi Most.
I may or may not keep it updated if I find it useful.

pnaomi@gmail.com

