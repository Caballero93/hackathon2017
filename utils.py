"""This module contains utilities that can be used from solution as
well as from framework.

"""

import json
import sys
import os
import zmq
from typing import Dict, Tuple, Union, Optional

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

class ResultsMessage:
    """Message that is sent back to the framework by the solution."""
    def __init__(self, one, two, three):
        self.one = one
        self.two = two
        self.three = three

class DataMessage:
    """Message that is sent by the framework to the solution."""
    def __init__(self, one, two, three):
        self.one = one
        self.two = two
        self.three = three

def bind_sub_socket(address: int, port: int) -> \
    Optional[Tuple[zmq.Socket, zmq.Context]]:
    """Make subscribe socket and return pair of socket itself and its
    context

    """
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
    """Same as bind_sub_socket but for publish socket"""
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

class Config():
    """Class that represents configuration file.

    It is initialized only once when this module is imported. The aim
    is to have only one instance of this class that could be imported
    wherever it is needed - CFG.

    """
    def __init__(self):
        """
        socket_in_port - port used by framework to send data to solution
        socket_out_port - port used by solution to send calculated data to framework
        in_address - IP address for socket_in_port
        out_address - IP address for socket_out_port
        """
        config = self.get_conf()
        self.in_port = config.get('in_port', None)
        self.out_port = config.get('out_port', None)
        self.in_address = config.get('in_address', None)
        self.out_address = config.get('out_address', None)
        self.results = config.get('results', None)

    @staticmethod
    def get_conf() -> Dict[str, Union[int, str]]:
        """Read configuration file to a dictionary."""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)

        except FileNotFoundError:
            print('Configuration file is not foud.' + 2*os.linesep +
                  'This script normally looks for config.json in current directory.',
                  file=sys.stderr)
            return None

# Unique configuration object that should be used everywhere
CFG = Config()
