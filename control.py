from utils import *
from typing import Optional

class Message:
    def __init__(one, two, three):
        self.one
        self.two
        self.three

class Control:
    def __init__(self,
                 in_port: Optional[int]=None, in_addr: Optional[int]=None,
                 out_port: Optional[int]=None, out_addr: Optional[int]=None):
        self.config = get_conf()
        self.in_port = in_port or self.config['socket_in_port']
        self.in_addr = in_addr or self.config['in_address']
        self.out_port = out_port or self.config['socket_out_port']
        self.out_addr = out_addr or self.config['out_address']
        self.in_socket, self.in_context = bind_sub_socket(self.in_addr,
                                                          self.in_port)
        self.out_socket, self.out_context = bind_pub_socket(self.out_addr,
                                                            self.out_port)

    def get_data(self) -> [dict]:
        while True:
            msg = self.in_socket.recv_pyobj()
            if not 'end' in msg:
                yield msg
            else:
                return

    def push_results(self, obj: Message) -> None:
        self.out_socket.send_pyobj(obj)
