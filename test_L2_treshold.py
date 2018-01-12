import webbrowser
from multiprocessing import Process
import run_solution as solution
import run_framework as framework
from hackathon.utils.utils import CFG
from hackathon.framework.http_server import prepare_dot_dir
import json

class Solution(object):
    def __init__(self, L2_treshold):
        self.p = Process(target=solution.run, args=('log', L2_treshold))
    def start(self):
        self.p.start()

    def join(self):
        self.p.join()

    def terminate(self):
        self.p.terminate()

class Framework(object):
    def __init__(self):
        self.p = Process(target=framework.run, args=('log',))
    def start(self):
        self.p.start()

    def join(self):
        self.p.join()

    def terminate(self):
        self.p.terminate()

if __name__ == '__main__':
    prepare_dot_dir()
    L2_treshold = 6.0
    results_list = []
    for i in range(2):
        solution_process = Solution(L2_treshold)
        solution_process.start()
        framework_process = Framework()
        framework_process.start()

        webbrowser.open('http://localhost:{}/viz.html'
                        .format(CFG.results_http_server_port))
        solution_process.join()
        framework_process.join()
        solution_process.terminate()
        framework_process.terminate()
        with open('./data/results.json', 'r') as f:
            data = json.load(f)
        final_res = data[7199]['overall']
        results_list.append((L2_treshold, final_res))
        L2_treshold += 0.5

    with open('test_L2_treshold.txt', 'a') as f:
        f.write(str(results_list))


