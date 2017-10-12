import json
import sys
import os
import zmq
from typing import Dict, Tuple, Union, Optional

def get_conf() -> Dict[str, Union[int, str]]:
    try:
        with open('config.json', 'r') as f:
            return json.load(f)

    except FileNotFoundError:
        print('Configuration file is not foud.' + 2*os.linesep +
              'This script normally looks for config.json in current directory.',
              file=sys.stderr)
        return None

def bind_sub_socket(address: int, port: int) -> \
    Optional[Tuple[zmq.Socket, zmq.Context]]:
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    try:
        socket.connect('tcp://{}:{}' .format(address, port))
        socket.setsockopt(zmq.SUBSCRIBE, b'')
        print('Subscribe socket connected at {}:{}.'.format(socket, port))
        return socket, context
    except Exception as e:
        print('Connection to socket at {}:{} has failed.'
              .format(address, port), file=sys.stderr)
        print(e)
        exit()

def bind_pub_socket(address: int, port: int) -> \
    Optional[Tuple[zmq.Socket, zmq.Context]]:
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    try:
        socket.bind("tcp://{}:{}".format(address, port))
        return socket, context
    except Exception as e:
        print('Connection to socket at {}:{} has failed.'
              .format(address, port), file=sys.stderr)
        print(e)
        exit()
