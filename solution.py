#!/usr/bin/env python
"""This module represents a dummy example of the solution that should
be provided by contestants

"""

from control import Control
from os.path import join
import sys
from utils import ResultsMessage, DataMessage, PVMode, TYPHOON_DIR

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestors."""
    print('D: received {}'.format(data.id))
    print('Worker doing its job, message is {} ...'.format(msg))
    print('D: is going to send {}'.format(data.id))

    return ResultsMessage(data_msg=msg,
                          load_one=False,
                          load_two=False,
                          load_three=False,
                          power_reference=0.0,
                          pv_mode=PVMode.SUPPLY)

if __name__ == '__main__':
    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
