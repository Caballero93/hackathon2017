#!/usr/bin/env python
"""This module represents Typhoon HIL framework that is used for
testing and rating of solutions.

"""

import time
from multiprocessing import Process
from typing import *
import zmq
from utils import *
from http_server import run as http_server_run

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

def get_physics_metrics(data: DataMessage, results: ResultsMessage,
                        spent_time: float, match: bool) \
                        -> Tuple[float, float]:
    """TODO: this function should be implemented by the team that define
    physics.

    """

    return 1, 1

def rater(socket: zmq.Socket, poller: zmq.Poller, data_msg: DataMessage) \
    -> None:
    """Calculate time spent by the solution in current cycle and physics
    mark for data_msg (if returned). Calculated data is being written
    in results file.

    """
    start = time.time()
    # poller.poll blocks until message is sent or for passed
    # milliseconds if message is not sent
    msgs = dict(poller.poll(
        None if CFG.DBGPhysics else CFG.max_results_wait * 1000))
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

        write_a_result(
            *get_physics_metrics(data, solution_response, spent, match))
    elif CFG.DBG:
        print('DBG: results are not sent in predefined interval of {}s.'
              .format(CFG.max_results_wait))

if __name__ == '__main__':
    data_emit_socket, _ = bind_pub_socket(CFG.in_address, CFG.in_port)
    result_gather_socket, _ = bind_sub_socket(CFG.out_address, CFG.out_port)
    results_poll = zmq.Poller()
    results_poll.register(result_gather_socket, zmq.POLLIN)

    # Run http server in separate process
    http = Process(target=http_server_run, args=())
    http.start()

    # Create results file, truncate if exists
    with open(CFG.results, 'w'):
        pass

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

    if CFG.shutdown_http_server:
        # Gracefully terminate HTTP server process that serves results
        # to visualization web page
        time.sleep(2)
        http.terminate()
        print('Simple HTTP server has stopped.')
    else:
        print('Simple HTTP server is still running...')
