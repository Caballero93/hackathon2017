"""This module facilitates communication with the framework component."""

from typing import Optional
from utils import *

__author__ = "Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

class Control:
    """Abstraction that represents connection between framework and
    solution.

    """
    def __init__(self,
                 in_port: Optional[int]=None, in_addr: Optional[int]=None,
                 out_port: Optional[int]=None, out_addr: Optional[int]=None):
        """Communication sockets can be given by address and port, if not
        configuration file is used.

        """
        self.in_socket, self.in_context = bind_sub_socket(
            in_addr or CFG.in_address,
            in_port or CFG.socket_in_port)
        self.out_socket, self.out_context = bind_pub_socket(
            out_addr or CFG.out_address,
            out_port or CFG.socket_out_port)

    def get_data(self) -> [dict]:
        """Get data from the framework.

        Generator containing data is being returned.

        """
        while True:
            msg = self.in_socket.recv_pyobj()
            if not msg.one == 1:
                yield msg
            else:
                return

    def push_results(self, obj: ResultsMessage) -> None:
        """Send message that contains results calculated by the solution back
        to the framework.

        """
        self.out_socket.send_pyobj(obj)
