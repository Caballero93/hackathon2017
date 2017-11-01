#!/usr/bin/env python
"""This module runs both your contestor's solution and framework."""

import subprocess
import sys
import webbrowser
from utils import CFG

if __name__ == '__main__':
    solution_example = 'solution.py'
    solution = sys.argv[1] if len(sys.argv) > 1 else solution_example

    subprocess.Popen(['python', solution, 'true'])
    subprocess.Popen(['python', 'framework.py', 'true'])

    webbrowser.open('http://localhost:{}/viz.html'
                    .format(CFG.results_http_server_port))
