"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
from scipy.optimize import minimize


def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py

    # Dummy result is returned in every cycle here
    def objective(x):
        return msg.buying_price * (msg.current_load - msg.solar_production - x[0])

    def constraint1(x):
        return msg.bessSOC - x[0] / 600 - 0.2

    def constraint2(x):
        return 1.0 - msg.bessSOC + x[0] / 600

    bnds = ((-6.0, 6.0),)
    con1 = {'type': 'ineq', 'fun': constraint1}
    con2 = {'type': 'ineq', 'fun': constraint2}
    cons = [con1, con2]
    x0 = [0]

    L1, L2, L3 = True, True, True
    p_bat = 0.0
    panel = PVMode.ON
    if not msg.grid_status:
        temp = msg.solar_production + 6 - msg.current_load
        if temp < 0:
            if temp > -0.3 * msg.current_load:
                L3 = False
            else:
                L2, L3 = False, False
        if msg.bessSOC < 0.56:
            L3 = False
        if msg.bessSOC < 0.2:
            L2, L3 = False, False
        if msg.solar_production > msg.current_load and msg.bessSOC > 0.99:
            panel = PVMode.OFF

    else:
        sol = minimize(objective, x0, method='SLSQP', bounds=bnds, constraints=cons)
        p_bat = float(sol.x[0])

    print("Results message: ",L1, L2, L3, p_bat, panel)


    return ResultsMessage(data_msg=msg,
                          load_one=L1,
                          load_two=L2,
                          load_three=L3,
                          power_reference=p_bat,
                          pv_mode=panel)


def run(args) -> None:
    prepare_dot_dir()
    #config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
