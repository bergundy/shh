from shh import Command, ls, grep, git

print '%r' % ~git.rev_parse(abbrev_ref='HEAD')

for l in ls(l=True) | grep.shh:
    print l

-(ls('-l') | grep('shh') > '/tmp/hey.txt')
print +(Command('/bin/cat') < '/tmp/hey.txt')
