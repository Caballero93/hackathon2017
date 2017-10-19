#!/usr/bin/env python
"""This module represents a dummy example of the solution that should
be provided by contestants

"""

from control import Control
from utils import ResultsMessage, DataMessage

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

def worker(msg: DataMessage) -> ResultsMessage:
    print('Worker doing its job, message is {} ...' \
          .format(msg))
    return ResultsMessage(msg, 0, 0, 0)

if __name__ == '__main__':
    cntrl = Control()

    for data in cntrl.get_data():
        print('D: received {}'.format(data.id))
        from time import sleep; sleep(16)
        print('D: sent {}'.format(data.id))
        cntrl.push_results(worker(data))
