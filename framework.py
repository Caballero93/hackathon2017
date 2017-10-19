#!/usr/bin/env python
"""This module represents Typhoon HIL framework that is used for
testing and rating of solutions.

"""

import os
import time
from utils import *
from typing import *
import zmq

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

def get_physics_metrics(data: DataMessage, results: ResultsMessage,
                        spent_time: float, match: bool) -> None:
    with open(CFG.results, 'a+') as f:
        f.write('{}:{} [{}]{}'
                .format(str(results), spent_time, match, os.linesep))

def rater(socket: zmq.Socket, poller: zmq.Poller, data_msg: DataMessage) \
    -> None:
    start = time.time()
    msgs = dict(poller.poll(CFG.max_results_wait * 1000))
    spent = time.time() - start

    if socket in msgs and msgs[socket] == zmq.POLLIN:
        solution_response = socket.recv_pyobj()

        match = True
        if solution_response.data_msg.id != data_msg.id:
            match = False
            spent = CFG.max_results_wait

        if CFG.DBG:
            print('DBG: {} {} received after {}s.'
                  .format('ADEQUATE' if match else 'INADEQUATE',
                          solution_response, spent))

        get_physics_metrics(data, solution_response, spent, match)
    elif CFG.DBG:
        print('DBG: Results are not sent in predefined interval of {}s.'
              .format(CFG.max_results_wait))

if __name__ == '__main__':
    data_emit_socket, _ = bind_pub_socket(CFG.in_address, CFG.in_port)
    result_gather_socket, _ = bind_sub_socket(CFG.out_address, CFG.out_port)
    results_poll = zmq.Poller()
    results_poll.register(result_gather_socket, zmq.POLLIN)

    lapse_time = CFG.framework_lapse_time or 1
    print('Framework is booting with the lapse time of {}s ...'
          .format(lapse_time))
    time.sleep(lapse_time)

    for i in range(CFG.samples_num):
        data = DataMessage(i, 0, 0, 0)

        if CFG.DBG:
            print('Framework emits {}'.format(data))

        data_emit_socket.send_pyobj(data)
        rater(result_gather_socket, results_poll, data)

    # Send terminating message to the solution
    data_emit_socket.send_pyobj(False)
