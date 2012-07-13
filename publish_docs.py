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

call(['git', 'checkout', 'master'], shell=True)
call(['make', '-C', 'docs', 'html'], shell=True)
call(['rm', '-rf', '/tmp/docs_html'], shell=True)
call(['cp', '-R', 'docs/_build/html', '/tmp/docs_html'], shell=True)
call(['git', 'checkout', 'gh-pages'], shell=True)
call(['rm', '-rf', 'docs'], shell=True)  # wtf!!  i can't do a rm -rf * for some reason
call(['rm', '-rf', 'sanetime'], shell=True)  # wtf!!  i can't do a rm -rf * for some reason
call(['cp', '-R', '/tmp/docs_html/*', '.'], shell=True)
call(['git', 'add', '.'], shell=True)
#call(['git', 'commit', '-a', '-v'])
#call(['git', 'push'])
#call(['git', 'checkout', 'master'])

