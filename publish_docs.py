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

call(['git', 'checkout', 'master'])
call(['cd', 'docs'])
call(['make', 'html'])
call(['cp', '-R', '_build/html', '/tmp/sanetime_docs_html'])
call(['cd', '..'])
call(['git', 'checkout', 'gh-pages'])
call(['cp', '-r', '/tmp/sanetime_docs_html', '.'])
call(['git', 'add', '.'])
call(['git', 'commit', '-a', '-v'])
call(['git', 'push'])
call(['git', 'checkout', 'master'])

