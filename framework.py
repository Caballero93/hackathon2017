import time
import random
from utils import *
from typing import *

if __name__ == '__main__':
    config = get_conf()
    socket, _ = bind_pub_socket(config['in_address'], config['socket_in_port'])

    # TODO: Handle results sent by solution
    while True:
        print('Socket publishing a message at {}:{} ...'
              .format(config['in_address'], config['socket_in_port']))

        if random.random() >= 0.95:
            socket.send_pyobj({'end': 1})
        else:
            socket.send_pyobj({'msg': 'hello!'})

        time.sleep(1)
