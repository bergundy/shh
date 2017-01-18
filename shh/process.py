from subprocess import Popen
from itertools import imap, chain
from operator import methodcaller
import subprocess
import pipes

try:
    from subprocess import DEVNULL  # py3k, thanks SO
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

PIPE = object()
STDOUT_TO = object()
STDOUT_APPEND_TO = object()
STDIN_FROM = object()
STDIN_FROM_STRING = object()


class Process(object):
    def __init__(self, *arguments):
        self.arguments = arguments

    @staticmethod
    def quote(arg):
        if arg is PIPE:
            return '|'
        elif arg is STDOUT_TO:
            return '>'
        elif arg is STDOUT_APPEND_TO:
            return '>>'
        elif arg is STDIN_FROM:
            return '<'
        elif arg is STDIN_FROM_STRING:
            return '<<<'
        else:
            return pipes.quote(arg)

    @staticmethod
    def fmt_keyword(kw, value):
        if value is False:
            return ()
        else:
            prefix = '-' if len(kw) == 1 else '--'
            formatted = prefix + kw.replace('_', '-')
            if value is True:
                return (formatted, )
            else:
                return (formatted, value)

    def __str__(self):
        return ' '.join(map(self.quote, self.arguments))

    def __call__(self, *arguments, **kwargs):
        if not arguments and not kwargs:
            return bool(self)
        keywords = (self.fmt_keyword(k, v) for k, v in kwargs.items())
        return Process(*(self.arguments + tuple(chain.from_iterable(keywords)) + arguments))

    def __getattr__(self, command):
        return self(command.replace('_', '-'))

    def __or__(self, other):
        if isinstance(other, Process):
            return Process(*(self.arguments + (PIPE,) + other.arguments))
        else:
            return other(str(self))

    def __gt__(self, f):
        return Process(*(self.arguments + (STDOUT_TO, f)))

    def __lt__(self, f):
        return Process(*(self.arguments + (STDIN_FROM, f)))

    def __rshift__(self, f):
        return Process(*(self.arguments + (STDOUT_APPEND_TO, f)))

    def __lshift__(self, _input):
        return Process(*(self.arguments + (STDIN_FROM_STRING, _input)))

    def __invert__(self):
        return subprocess.check_output(str(self), shell=True).strip()

    def __neg__(self):
        return subprocess.check_call(str(self), stdout=DEVNULL, shell=True)

    def __pos__(self):
        return subprocess.check_call(str(self), shell=True)

    def __bool__(self):
        try:
            subprocess.check_call(str(self), shell=True)
            return True
        except subprocess.CalledProcessError:
            return False

    __nonzero__ = __bool__

    def __iter__(self):
        return readlines(str(self))


def readlines(command):
    p = Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in imap(methodcaller('strip'), iter(p.stdout.readline, '')):
        yield line
    p.wait()
