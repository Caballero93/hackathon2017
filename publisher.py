import zmq
import time
import sys
import os
import json
import random
from utils import *

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    global PORT
    PORT = get_socket_port()
    socket.bind("tcp://*:{}".format(PORT))

    while True:
        print('Socket publishing a message on port {} ...'.format(PORT))

        if random.random() >= 0.95:
            socket.send_pyobj({'end': 1})
        else:
            socket.send_pyobj({'msg': 'hello!'})

        time.sleep(1)
