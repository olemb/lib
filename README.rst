lib.py
======

My personal collection of useful Python functions. This lives in
``~/lib/python``.

Feel free to cut and paste into your own projects.


Examples
--------

Contextmanagers tmpdir() and chdir()::

    >>> import os
    >>> from lib import tmpdir, chdir
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
    >>> os.chdir('/tmp/tmpdRzm2V')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    OSError: [Errno 2] No such file or directory: '/tmp/tmpdRzm2V'

inpipe() and stripped()::

    >>> import os
    >>> from lib import inpipe, stripped
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

    >>> from lib import outpipe
    >>> 
    >>> args = ['vorbiscomment', '-w', '-c', '-', '.ogg']
    >>> with outpipe(args, nl=True) as write:
    ...     write('artist=Kepa Junkera')
    ...     write('album=Bilbao 00:00h')
    ...     write('title=Arin Qubec')
    ...     write('tracknumber=1')
    ...    
    
Inpipe and outpipe will encode/decode the data. The default encoding
is 'utf-8', but this can be overriden by calling inpipe(args,
encoding='latin1') etc.

env()::

    >>> from lib import env
    >>>
    >>> env('$USER lives in $HOME')
    'olemb lives in /home/olemb'
    >>> 


Author: Ole Martin Bjørndalen - ombdalen@gmail.com - http://nerdly.info/ole/

License: MIT
