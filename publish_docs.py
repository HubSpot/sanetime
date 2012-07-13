#!/usr/bin/env python
import subprocess

def call(args, shell=False):
    if isinstance(args, basestring):
        pcmd = args
    else:
        pcmd = ' '.join(args)
    print("== attempting == %s =="%pcmd)
    if subprocess.call(args, shell=shell):
        print("== !problem!  == %s ==" % pcmd)
        exit(1)
    print("== done       == %s ==" % pcmd)
    print

call(['git', 'checkout', 'master'])
call(['make', '-C', 'docs', 'html'])
call(['rm', '-rf', '/tmp/docs_html'])
call(['cp', '-R', 'docs/_build/html', '/tmp/docs_html'])
call(['git', 'checkout', 'gh-pages'])
call('rm -rf *', True) 
call('cp -R /tmp/docs_html/* .', True)
call(['git', 'add', '.'])
call(['git', 'commit', '-a', '-v'])
call(['git', 'push'])
call(['git', 'checkout', 'master'])

