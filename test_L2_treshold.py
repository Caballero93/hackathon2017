import webbrowser
from multiprocessing import Process
import run_solution as solution
import run_framework as framework
from hackathon.utils.utils import CFG
from hackathon.framework.http_server import prepare_dot_dir
import json

class Solution(object):
    def __init__(self, L2_treshold, P_BATT):
        self.p = Process(target=solution.run, args=('log', L2_treshold, P_BATT))
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
    L2_treshold = 6.5
    results_list = []
    webbrowser.open('http://localhost:{}/viz.html'
                    .format(CFG.results_http_server_port))
    for i in range(2):
        P_BATT = 1.0
        for j in range(11):
            solution_process = Solution(L2_treshold, P_BATT)
            solution_process.start()
            framework_process = Framework()
            framework_process.start()

            solution_process.join()
            framework_process.join()
            solution_process.terminate()
            framework_process.terminate()

            with open('./data/results.json', 'r') as f:
                data = json.load(f)
            final_res = data[7199]['overall']
            results_list.append((L2_treshold, P_BATT, final_res))
            P_BATT += 0.5

        L2_treshold += 0.1

    # P_BATT = 4.0
    # for i in range(11):
    #     solution_process = Solution(L2_treshold, P_BATT)
    #     solution_process.start()
    #     framework_process = Framework()
    #     framework_process.start()
    #
    #     solution_process.join()
    #     framework_process.join()
    #     solution_process.terminate()
    #     framework_process.terminate()
    #
    #     with open('./data/results.json', 'r') as f:
    #         data = json.load(f)
    #     final_res = data[7199]['overall']
    #     results_list.append((L2_treshold, P_BATT, final_res))
    #     L2_treshold += 0.1

    with open('test_L2_treshold.txt', 'a') as f:
        for el in results_list:
            res = str(el) + '\n'
            f.write(res)


