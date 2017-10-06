import json
import sys
import os

def get_socket_port():
    try:
        with open('config.json', 'r') as f:
            p = json.load(f)['socket_port']

        if p:
            return p

        print('There is no \"socket_port\" key in configuration file.',
              file=sys.stderr)
        exit()

    except FileNotFoundError:
        print('Configuration file is not foud.' + 2*os.linesep +
              'This script normally looks for config.json in current directory.',
              file=sys.stderr)
