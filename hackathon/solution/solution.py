"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
from pulp import *
from hackathon.energy.rating import PENAL_L1_CONT, PENAL_L1_INIT, PENAL_L2_CONT, PENAL_L2_INIT, PENAL_L3_CONT

# define previous load states
global L1_old
L1_old = True
global L2_old
L2_old = True
global L3_old
L3_old = True

def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py

    # define problem parameters
    LOAD_1 = 0.2 * msg.current_load
    LOAD_2 = 0.5 * msg.current_load
    LOAD_3 = 0.3 * msg.current_load
    P_pv = msg.solar_production
    price = msg.buying_price
    global L1_old
    global L2_old
    global L3_old

    # initialize control variables
    L1, L2, L3 = True, True, True
    p_bat = 0.0
    panel = PVMode.ON

    # If grid is not active - SURVIVE
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
        # define decision variables
        MILP_P_bat = LpVariable("MILP_P_bat", -6.0, 6.0, LpContinuous)
        MILP_L1 = LpVariable("MILP_L1", 0, 1, LpBinary)
        MILP_L2 = LpVariable("MILP_L2", 0, 1, LpBinary)
        MILP_L3 = LpVariable("MILP_L3", 0, 1, LpBinary)

        # define MILP problem
        prob = LpProblem("Problem1", LpMinimize)

        # add objective function first:
        prob += price * (MILP_L1*LOAD_1 + MILP_L2*LOAD_2 + MILP_L3*LOAD_3 - P_pv - MILP_P_bat) \
                + (1-MILP_L1) * PENAL_L1_CONT + (1-MILP_L2) * PENAL_L2_CONT + (1-MILP_L3) * PENAL_L3_CONT \
                + L1_old * (1-MILP_L1) * PENAL_L1_INIT + L2_old * (1-MILP_L2) * PENAL_L2_INIT

        # add constraints:
        prob += MILP_P_bat/600 + msg.bessSOC <= 1
        prob += MILP_P_bat/600 + msg.bessSOC >= 0.2

        # solve the problem:
        prob.solve()

        # print status:
        print("========================================================")
        print("Status: ", LpStatus[prob.status])
        print("========================================================")

        # assign values to control variables
        for v in prob.variables():
            if v.name == 'MILP_P_bat':
                p_bat = v.varValue
            elif v.name == 'MILP_L1':
                L1 = bool(v.varValue)
            elif v.name == 'MILP_L2':
                L2 = bool(v.varValue)
            elif v.name == 'MILP_L3':
                L3 = bool(v.varValue)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(str(p_bat) + "\t" + str(L1) + '\t' + str(L2) + '\t' + str(L3) + '\t' + str(panel))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    # Refresh old load states
    L1_old = L1
    L2_old = L2
    L3_old = L3

    # Dummy result is returned in every cycle here
    return ResultsMessage(data_msg=msg,
                          load_one=L1,
                          load_two=L2,
                          load_three=L3,
                          power_reference=p_bat,
                          pv_mode=panel)


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
