olelib.py
=========

Various useful functions.


Examples
--------

Contextmanagers tmpdir() and chdir()::

    >>> import os
    >>> from olelib import tmpdir, chdir
    >>>
    >>> with tmpdir() as t:
    ...     with chdir(t):
    ...             print(t)
    /tmp/tmpdRzm2V
    ...             print(os.getcwd())
    /tmp/tmpdRzm2V
    ...             os.mkdir('these')
    ...             os.mkdir('temporary')
    ...             os.mkdir('dirs')
    ...             os.mkdir('will')
    ...             os.mkdir('be')
    ...             os.mkdir('deleted')
    ...
    >>>

inpipe() and stripped()::

    >>> import os
    >>> from olelib import inpipe, stripped
    >>>
    >>> for line in stripped(inpipe(['ls'])):
    ...     print(repr(line))
    ...
    'LICENSE'
    'olelib.py'
    'olelib.pyc'
    'README.rst'
    >>> 

outpipe()::

    >>> from olelib import outpipe
    >>> 
    >>> args = ['vorbiscomment', '-w', '-c', '-', '.ogg']
    >>> with outpipe(args, nl=True) as write:
    ...     write('artist=Kepa Junkera\n')
    ...     write('album=Bilbao 00:00h\n')
    ...     write('title=Arin Qubec\n')
    ...     write('tracknumber=1\n')
    ...    
    
Inpipe and outpipe will encode/decode the data. The default encoding
is 'utf-8', but this can be overriden by calling inpipe(args,
encoding='latin1') etc.

env()::

    >>> from olelib import env
    >>>
    >>> env('$USER lives in $HOME')
    'olemb lives in /home/olemb'
    >>> 

Author: Ole Martin Bjørndalen - ombdalen@gmail.com - http://nerdly.info/ole/

License: MIT


