#!/usr/bin/env python
"""This script simply runs typhoons framework"""

import sys
import os
from hackathon.framework.framework import run
from hackathon.utils.utils import TYPHOON_DIR
from hackathon.framework.http_server import prepare_dot_dir

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

if __name__ == '__main__':
    prepare_dot_dir()

    import generate_profiles

    run(sys.argv)
