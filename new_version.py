#!/usr/bin/env python
import subprocess

def call(args):
    cmd = ' '.join(args)
    print("== attempting == %s =="%cmd)
    if subprocess.call(args):
        print("== !problem!  == %s ==" % cmd)
        exit(1)
    print("== done       == %s ==" % cmd)
    print

version = [line for line in open('setup.py').read().split('\n') if line.startswith('VERSION = ')][0].split(' ')[-1].strip('"').strip("'")

call(['git', 'commit', '-v'])
call(['git', 'push'])
call(['git', 'tag', '-a', 'v%s'%version, '-m="version bump"'])
call(['git', 'push', '--tags'])
call(['python', 'setup.py', 'sdist', 'upload'])

