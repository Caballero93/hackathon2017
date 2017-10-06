import zmq
import json
import os
import sys
import traceback
from utils import *

def worker(msg):
    print('Worker doing its job, message is {} ...' \
          .format(msg))

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    global PORT
    PORT = get_socket_port()

    try:
        socket.connect ('tcp://localhost:{}'.format(PORT))
        socket.setsockopt(zmq.SUBSCRIBE, b'')
        print('Socket connected on port {}.'.format(PORT))
    except Exception as e:
        print('Connection to socket on port {} has failed.'.format(PORT),
              file=sys.stderr)
        print(e)
        exit()

    while True:
        msg = socket.recv_pyobj()

        if 'end' in msg:
            print('Publisher sent an end message.')
            exit()

        worker(msg)
