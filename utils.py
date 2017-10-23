"""This module contains utilities that can be used from solution as
well as from framework.

"""

import sys
import os
from functools import partial
from configparser import ConfigParser
import zmq
from typing import Dict, Tuple, Union, Optional

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

class DataMessage:
    """Message that is sent by the framework to the solution."""
    def __init__(self, id, one, two, three):
        self.id = id
        self.one = one
        self.two = two
        self.three = three

    def __str__(self):
        return "id={}, one={}, two={}, three={}" \
            .format(self.id, self.one, self.two, self.three)

class ResultsMessage:
    """Message that is sent back to the framework by the solution."""
    def __init__(self, data_msg: DataMessage, one: int, two: int, three: int) \
        -> None:
        self.data_msg = data_msg
        self.one = one
        self.two = two
        self.three = three

    def __str__(self):
        return "{}: one={}, two={}, three={}" \
            .format(self.data_msg, self.one, self.two, self.three)

def bind_sub_socket(address: str, port: int) -> \
    Optional[Tuple[zmq.Socket, zmq.Context]]:
    """Make subscribe socket and return pair of socket itself and its
    context

    """
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    try:
        socket.connect('tcp://{}:{}' .format(address, port))
        socket.setsockopt(zmq.SUBSCRIBE, b'')
        print('Subscribe socket connected at {}:{}.'.format(address, port))
        return socket, context
    except Exception as e:
        print('Connection to socket at {}:{} has failed.'
              .format(address, port), file=sys.stderr)
        print(e)
        exit()

def bind_pub_socket(address: str, port: int) -> \
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

def safe_int(s: str) -> Optional[int]:
    try:
        return int(s)
    except:
        return None

def safe_bool(s: str) -> Optional[bool]:
    if s == 'True':
        return True
    else:
        return None

class Config:
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
        conf = self.get_conf()
        sockets = partial(self.get_from, conf, 'sockets')
        results = partial(self.get_from, conf, 'results')
        framework = partial(self.get_from, conf, 'framework')

        self.in_port = safe_int(sockets('inPort')) # type: Optional[int]
        self.out_port = safe_int(sockets('outPort')) # type: Optional[int]
        self.in_address = sockets('inAddress') # type: Optional[str]
        self.out_address = sockets('outAddress') # type: Optional[str]
        self.results = results('resultsFile') # type: Optional[str]
        self.results_http_server_port = safe_int(
            results('resultsHTTPServerPort')) # type: Optional[int]
        self.shutdown_http_server = safe_bool(
            results('shutdownHTTPServer')) # type: Optional[bool]
        self.samples_num = safe_int(framework('samplesNum')) # type: Optional[int]
        self.framework_lapse_time = safe_int(
            framework('frameworkLapseTime')) # type: Optional[int]
        self.max_results_wait = safe_int(
            framework('maxResultsWait')) # type: Optional[int]
        self.DBG = safe_bool(framework('DBG')) # type: Optional[bool]

    @staticmethod
    def get_conf() -> ConfigParser:
        """Read configuration file to a dictionary."""
        conf_fname = 'params.conf'

        try:
            with open(conf_fname, 'r'):
                pass
        except FileNotFoundError:
            print('Configuration file is not foud.' + 2*os.linesep +
                  'This script normally looks for params.conf in current directory.',
                  file=sys.stderr)
            return None

        cp = ConfigParser()
        cp.read(conf_fname)
        return cp

    @staticmethod
    def get_from(cp: ConfigParser, section: str, key: str) \
        -> Optional[str]:
        try:
            return cp[section][key]
        except:
            return None

# Unique configuration object that should be used everywhere
CFG = Config()
