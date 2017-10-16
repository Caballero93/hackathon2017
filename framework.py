#!/usr/bin/env python
"""This module represents Typhoon HIL framework that is used for
testing and rating of solutions.

"""

from multiprocessing import Process
from time import time, sleep
import random
from utils import *
from typing import *
import zmq

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

def get_physics_metrics(results: ResultsMessage, spent_time: float) -> None:
    # TODO: Make this file append suitable for concurrency
    with open(CFG.results, 'a+') as f:
        f.write('{}:{}'.format('result 1', spent_time))

def rater(socket: zmq.Socket) -> None:
    start = time()
    solution_response = socket.recv_pyobj()
    spent = time() - start

    get_physics_metrics(solution_response, spent)

if __name__ == '__main__':
    data_emit_socket, _ = bind_pub_socket(CFG.in_address, CFG.in_port)
    result_gather_socket, _ = bind_sub_socket(CFG.out_address,
                                              CFG.out_port)

    processes = []
    while True:
        print('Socket publishing a message at {}:{} ...'
              .format(CFG.in_address, CFG.in_port))

        if random.random() >= 0.95:
            data_emit_socket.send_pyobj(DataMessage(1, 0, 0))
        else:
            data_emit_socket.send_pyobj(DataMessage(0, 0, 0))

        # Spawn process which performs calculations on framework's side
        p = Process(target=rater, args=(result_gather_socket, ))
        p.start()
        # TODO: These processes should be joined at some
        # time. Otherwise they ramain dangle (zombie process) and
        # overflow the CPU.
        processes.append(p)

        sleep(1)
