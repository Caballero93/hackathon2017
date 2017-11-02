#!/usr/bin/env python
"""This module represents a dummy example of the solution that should
be provided by contestants

"""

import sys
import os
from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    print('D: received {}'.format(msg.id))
    print('Worker doing its job, message is {} ...'.format(msg))
    print('D: is going to send {}'.format(msg.id))

    # Dummy result is returned in every cycle here
    return ResultsMessage(data_msg=msg,
                          load_one=True,
                          load_two=True,
                          load_three=True,
                          power_reference=0.0,
                          pv_mode=PVMode.ON)

def run(args) -> None:
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))


if __name__ == '__main__':
    run(sys.argv)
