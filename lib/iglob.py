# -*- coding: utf-8 -*-                                                                  

"""                                                                                      
Functions for dealing with mixed-case files from case-preserving file systems.

Todo:

  - handle patterns that already have brackets
  - better documentation

Latest version of this file:

   https://gist.github.com/olemb/ifiles
"""

from __future__ import print_function
import os
import glob
import fnmatch

__author__ = 'Ole Martin Bjørndalen'
__email__ = 'ombdalen@gmail.com'
__license__ = 'MIT'


def ipat(pat):
    """Convert glob pattern to case insensitive form."""

    (dirname, pat) = os.path.split(pat)

    # Convert '/path/to/test.fpt' => '/path/to/[Tt][Ee][Ss][Tt].[]'                                                                              
    newpat = ''
    for c in pat:
        if c.isalpha:
            u = c.upper()
            l = c.lower()
            if u != l:
                newpat = newpat + '[' + u + l + ']'
            else:
                newpat += c
        else:
            newpat += c

    newpat = os.path.join(dirname, newpat)

    return newpat

def ifnmatch(name, pat):
    """Case insensitive version of fnmatch.fnmatch()"""
    return fnmatch.fnmatch(name, ipat(pat))

def iglob(pat):
    """Case insensitive version of glob.glob()"""
    return glob.glob(ipat(pat))

def ifind(pat, ext=None):
    """Look for a file in a case insensitive way. Returns filename it
    a matching file was found, or None if it was not."""

    if ext:
        pat = os.path.splitext(pat)[0] + ext

    files = iglob(pat)
    if files:
        return files[0]  # Return an arbitrary file                                                                                              
    else:
        return None

def iglob(pat):
    """Case insensitive version of glob.glob()"""
    return glob.glob(ipat(pat))

if __name__ == '__main__':
    print(ipat('mixedcase'))  # => "[Mm]m[Ii]i[Xx]x[Ee]e[Dd]d[Cc]c[Aa]a[Ss]s[Ee]e"
    print(ifnmatch('test', 'test'))  # => True
    print(ifnmatch('miXEdCaSe', 'mixedcase'))  # => True
    print(ifnmatch('CAMELCASE/CamelCase', 'CamelCase/UPPERCASE'))  # => False
    print(ifind(('/etc/PASSwd')))  # => True or false depending on your OS
    print(ipat(ipat('This will fail')))  # [[Tt][Tt]][[Hh][Hh]] ... etc. => 

__all__ = ['ipat', 'ifnmatch', 'iglob', 'ifind']
