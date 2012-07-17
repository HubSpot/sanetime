#!/usr/bin/env python
import subprocess
import sanetime

def call(args):
    cmd = ' '.join(args)
    print("== attempting == %s =="%cmd)
    if subprocess.call(args):
        print("== !problem!  == %s ==" % cmd)
        exit(1)
    print("== done       == %s ==" % cmd)
    print

call(['git', 'commit', '-v'])
call(['git', 'push'])
call(['git', 'tag', '-a', 'v%s'%sanetime.__version__, '-m="version bump"'])
call(['git', 'push', '--tags'])
call(['python', 'setup.py', 'sdist', 'upload'])

