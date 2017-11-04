#!/usr/bin/env python
import sys
import os
import subprocess
import shutil

def rm_r(path: str) -> None:
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.path.isdir(f):
            rm_r(f)
        else:
            os.remove(f)

if __name__ == '__main__':
    theirs = 'hackathon2017.their'
    subprocess.run(['git', 'clone', sys.argv[1], theirs])

    # Remove ours requirements file
    os.remove('requirements.txt')
    # Get theirs
    shutil.copyfile(os.path.join(theirs, 'requirements.txt'),
                    'requirements.txt')

    # Remove our hackathon/solution
    shutil.rmtree(os.path.join('hackathon', 'solution'))
    # Get their hackathon/solution
    shutil.copytree(os.path.join(theirs, 'hackathon', 'solution'),
                    os.path.join('hackathon', 'solution'))

    # Remove their repository completely
    rm_r(theirs)

    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

    subprocess.run(['python', 'run.py'])
