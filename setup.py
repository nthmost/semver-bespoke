from setuptools import setup, find_packages
import os

setup (
       name = 'semver-bespoke',
       version = '0.1.0',
       zip_safe = False,
       packages = find_packages(),
       entry_points = { 'console_scripts': [
                        'semver = semver.console:main',
                        ] 
                    }, 
       setup_requires = [
            # add things here to force installation ahead of stuff in install_requires
            ],
       install_requires = [
            'docopt',       #for happy docstring/CLI-option marriage.
            'ipython',      #interactive consoles
            'pytest',       #test harness
            ],
     )
