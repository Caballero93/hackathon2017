#!/usr/bin/env python
"""This module represents a dummy example of the solution that should
be provided by contestants

"""

from control import Control
from utils import ResultsMessage

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

def worker(msg):
    print('Worker doing its job, message is {} ...' \
          .format(msg))
    return ResultsMessage(0, 0, 0)

if __name__ == '__main__':
    cntrl = Control()

    for data in cntrl.get_data():
        print('DBG: received {}'.format(data.one))
        from time import sleep; sleep(3)
        cntrl.push_results(worker(data))
