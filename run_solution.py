#!/usr/bin/env python
"""This module represents a dummy example of the solution that should
be provided by contestants

"""

import sys
from hackathon.solution.solution import run
from hackathon.framework.http_server import prepare_dot_dir

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

if __name__ == '__main__':
    prepare_dot_dir()

    run(sys.argv)
