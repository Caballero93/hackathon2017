"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
from scipy.optimize import minimize

global BESS_BELOW
BESS_BELOW = False
def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py
    # Dummy result is returned in every cycle here
    global BESS_BELOW
    if msg.bessSOC >= 0.2:
        BESS_BELOW = False
    def objective(x):
        return msg.buying_price * (msg.current_load - msg.solar_production - x[0])

    def constraint1(x):
        return msg.bessSOC - x[0] / 600 - 0.2

    def constraint2(x):
        return 1.0 - msg.bessSOC + x[0] / 600

    bnds = ((- 6.0, 6.0),)
    con1 = {'type': 'ineq', 'fun': constraint1}
    con2 = {'type': 'ineq', 'fun': constraint2}
    cons = [con1, con2]
    x0 = [0]

    L1, L2, L3 = True, True, True
    p_bat = 0.0
    panel = PVMode.ON
    if not msg.grid_status:
        if msg.bessSOC < 0.2:
            BESS_BELOW = True
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
        if msg.solar_production > msg.current_load and msg.bessSOC == 1:
             panel = PVMode.OFF

    else:
        if msg.buying_price == 3:
            if msg.bessSOC != 1:
                p_bat = -6.0
            else:
                p_bat = 0.0
        else:
            if BESS_BELOW:
                p_bat = -6.0
            else:
                sol = minimize(objective, x0, method='SLSQP', bounds=bnds, constraints=cons)
                if sol.success:
                    p_bat = float(sol.x[0])
                else:
                    p_bat = 0.0
                print(sol.success)
                print("===============================================================")

    print(str(BESS_BELOW))
    print("Results message: ", L1, L2, L3, p_bat, panel)

    return ResultsMessage(data_msg=msg,
                          load_one=L1,
                          load_two=L2,
                          load_three=L3,
                          power_reference=p_bat,
                          pv_mode=panel)


def run(args) -> None:
    prepare_dot_dir()
    # config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
