from subprocess import Popen
from itertools import imap
from operator import methodcaller
import subprocess
import pipes


PIPE = object()
STDOUT_TO = object()


class Process(object):
    def __init__(self, arguments):
        self.arguments = arguments

    @staticmethod
    def quote(arg):
        if arg is PIPE:
            return '|'
        elif arg is STDOUT_TO:
            return '>'
        else:
            return pipes.quote(arg)

    def __str__(self):
        return ' '.join(map(self.quote, self.arguments))

    def __call__(self, *arguments):
        return Process(self.arguments + arguments)

    def __or__(self, other):
        if isinstance(other, Process):
            return Process(self.arguments + (PIPE,) + other.arguments)
        else:
            return other(str(self))

    def __invert__(self):
        return subprocess.check_call(str(self), shell=True)

    def __neg__(self):
        return subprocess.check_output(str(self), shell=True)

    def __pos__(self):
        return readlines(str(self))

    def __gt__(self, f):
        return Process(self.arguments + (STDOUT_TO, f))


class Spawner(object):
    def __getattr__(self, command):
        return Process((command,))

    def __call__(self, *arguments):
        return Process(arguments)


def readlines(command):
    p = Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in imap(methodcaller('strip'), iter(p.stdout.readline, '')):
        yield line
    p.wait()


spawn = Spawner()
ls = spawn.ls
grep = spawn.grep
echo = spawn.echo


for l in ls('-l', '.') | grep('shh') | readlines:
    print l

~(ls('-l') | grep('shh') > '/tmp/hey.txt')
print -echo('hey', 'ho')
print list(+spawn('/bin/cat', '/tmp/hey.txt'))
