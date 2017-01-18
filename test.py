from shh import Command, ls, grep, git


def test():
    command = git.rev_parse(abbrev_ref='HEAD')
    assert str(command) == 'git rev-parse --abbrev-ref HEAD'
    assert ~command == 'master'
    assert not grep('ahfsfwewgwg' * 2)(__file__)
    assert grep.ahfsfwewgwg(__file__) and ls()
    assert sum(1 for _ in ls(l=True) | grep.shh) == 1

    -(ls('-l') | grep('shh') > '/tmp/hey.txt')
    -(ls('-l') | grep('shh') >> '/tmp/hey.txt')

    assert len(list(Command('/bin/cat') < '/tmp/hey.txt')) == 2
    assert ~(Command('/bin/cat') << 'heh') == 'heh'
