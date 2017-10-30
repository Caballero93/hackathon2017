#!/usr/bin/env python
"""This module represents a dummy example of the solution that should
be provided by contestants

"""

from control import Control
from utils import ResultsMessage, DataMessage, PVMode

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestors."""
    print('D: received {}'.format(data.id))
    print('Worker doing its job, message is {} ...'.format(msg))
    from time import sleep; sleep(1)
    print('D: is going to send {}'.format(data.id))

    return ResultsMessage(msg, False, False, False, 0.0, PVMode.SUPPLY)

if __name__ == '__main__':
    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
