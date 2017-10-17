#!/usr/bin/env python
"""This module represents Typhoon HIL framework that is used for
testing and rating of solutions.

"""

import os
from time import time, sleep
from utils import *
from typing import *
import zmq

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

def get_physics_metrics(results: ResultsMessage, spent_time: float) -> None:
    with open(CFG.results, 'a+') as f:
        f.write('{}:{}{}'.format(ResultsMessage, spent_time, os.linesep))

def rater(socket: zmq.Socket) -> None:
    start = time()
    solution_response = socket.recv_pyobj()
    spent = time() - start

    get_physics_metrics(solution_response, spent)

if __name__ == '__main__':
    data_emit_socket, _ = bind_pub_socket(CFG.in_address, CFG.in_port)
    result_gather_socket, _ = bind_sub_socket(CFG.out_address, CFG.out_port)

    lapse_time = CFG.framework_lapse_time or 1
    print('Framework is booting with the lapse time of {}s ...'
          .format(lapse_time))
    sleep(lapse_time)

    for i in range(CFG.samples_num):
        print('Socket publishing a message at {}:{} ...'
              .format(CFG.in_address, CFG.in_port))

        data_emit_socket.send_pyobj(DataMessage(i, 0, 0))
        rater(result_gather_socket)

        sleep(1)
