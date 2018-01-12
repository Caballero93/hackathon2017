import webbrowser
from multiprocessing import Process
import run_solution as solution
import run_framework as framework
from hackathon.utils.utils import CFG
from hackathon.framework.http_server import prepare_dot_dir
import json

if __name__ == '__main__':
    prepare_dot_dir()
    L2_treshold = 7.0
    results_list = []
    solution = Process(target=solution.run, args=('log', L2_treshold))
    solution.start()
    framework = Process(target=framework.run, args=('log',))
    framework.start()

    webbrowser.open('http://localhost:{}/viz.html'
                    .format(CFG.results_http_server_port))
    solution.join()
    framework.join()
    with open('./data/results.json', 'r') as f:
        data = json.load(f)
    final_res = data[7199]['overall']
    results_list.append((L2_treshold, final_res))

    with open('test_L2_treshold.txt', 'a') as f:
        res = str(results_list) + "\n"
        f.write(res)
