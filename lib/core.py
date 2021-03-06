import os
import sys
import stat
import string
import shutil
import tempfile
import argparse
import subprocess
from collections import OrderedDict
from contextlib import contextmanager

py3 = sys.version_info.major >= 3


class RunCommandException(Exception):
    pass

# Just a shortcut
run = subprocess.check_call


def inpipe(args, encoding='utf-8'):
    """
    Run a command and yield each line from its standard output.

    Usage:

    for line in inpipe(['ls', '/etc/']):
        print(line)

    lines = list(inpipe(['ls', '/etc/']))
    """

    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in p.stdout:
        if py3:
            line = str(line, encoding)
        else:
            line = unicode(line, encoding)

        yield line 


@contextmanager
def outpipe(args, addnl=False, encoding='utf-8'):
    """
    Context manager which runs the command with args
    and reads from stdin. Yields a function that writes
    data to the pipe.
    
    If addnl=True, a newline is added to each
    string written.

    Usage:

    with outpipe(['tr', 'a-z', 'A-Z']) as write:
        write('Hello pipe!\n')  => HELLO PIPE!
    """

    # Todo: this doesn't work

    def write(text):
        if addnl:
            text += '\n'

        data = text.encode(encoding)
        p.stdin.write(data)
        p.stdin.flush()

    p = subprocess.Popen(args, stdin=subprocess.PIPE)

    yield write

    # p.kill()


@contextmanager
def outfile(filename, nl=False, encoding='utf-8'):
    """
    Context manager which opens a file and yield a
    function which writes text to the file.

    If nl=True, a newline is added to each
    string written.

    Usage:

    with outfile('foo.txt', nl=True) as write:
        for i in range(1, 100+1):
            write('This is line {0}!'.format(i))
    """

    def write(text):
        if nl:
            text += '\n'

        data = text.encode(encoding)
        f.write(data)
        f.flush()

    f = open(filename, 'wb')

    yield write

    f.close()


def stripped(seq):
    """                       
    Apply str.strip() to all strings in sequence
    Usage:                                                                             
 
    >>> for line in stripped(inpipe(['ls'])):
    ...     print(repr(line))
    ...
    'LICENSE'
    'olelib.py'
    'olelib.pyc'
    'README.rst'
    """

    for s in seq:
        yield s.strip()


@contextmanager
def tmpdir(suffix='', prefix='tmp', dir=None):
    dirname = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
    yield dirname
    shutil.rmtree(dirname)


@contextmanager
def chdir(dirname):
    old = os.getcwd()
    os.chdir(dirname)
    yield old
    os.chdir(old)


def isexec(path):
    """
    Return True if path is an executable file
    """

    if not os.path.isfile(path):
        return False

    mode = os.stat(path).st_mode
    if mode & stat.S_IEXEC:
        return True

    return False


def newext(filename, ext):
    """
    Return filename with a new extension.
    Usage:

    newname = newext('foo.flac', '.wav')  => 'foo.wav'
    """

    return os.path.splitext(filename)[0] + ext
    

def getext(filename):
    """
    Return the extension of a filename.
    """

    return os.path.splitext(filename)[1]


def variable_expander(vars, safe=False):
    """
    Return a function which expands
    $foo style variables in a text using
    values from the mapping 'vars'.

    If safe=False (the default) a KeyError
    will be raised if the variable name
    is not found in the mapping. If safe=True,
    the variable will instead be left in
    the text.

    Usage:

    import os

    env = variable_expander(os.environ)
    print(env("Today I found out that $USER's editor is $EDITOR"))
    """

    def expandvars(text):
        t = string.Template(text)
        if safe:
            return t.safe_substitute(vars)
        else:
            return t.substitute(vars)

    return expandvars


env = variable_expander(os.environ)
