#!/usr/bin/env python
"""This script simply runs typhoons framework"""

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

import sys
import os
from hackathon.framework.framework import run
from hackathon.utils.utils import TYPHOON_DIR

if __name__ == '__main__':
    run(sys.argv)
