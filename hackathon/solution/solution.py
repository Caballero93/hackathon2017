"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir


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
    global flag_solar

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
            flag_solar = True
            #panel = PVMode.OFF
        if flag_solar:
            panel = PVMode.OFF
    else:
        flag_solar = False
        if msg.buying_price == 3:
            if msg.bessSOC != 1:
                p_bat = -1.5
            else:
                p_bat = 0.0
        else:
            # Calculate MILP problem coefficients:
            L1_COEF = price * LOAD_1 / 60 - L1_old * PENAL_L1_INIT - PENAL_L1_CONT
            L2_COEF = price * LOAD_2 / 60 - L2_old * PENAL_L1_INIT - PENAL_L2_CONT
            L3_COEF = price * LOAD_3 / 60 - PENAL_L3_CONT

            # Assign decision variables:
            if L1_COEF > 0:
                L1 = False
            if L2_COEF > 0:
                L2 = False
            if L3_COEF > 0:
                L3 = False
            p_bat = 6.0

            #Protection from discharging the battery below SOC treshold:
            if msg.bessSOC - p_bat/600 < 0.2:
                p_bat = 600 * (msg.bessSOC - 0.2)

        real_load = L1 * LOAD_1 + L2 * LOAD_2 + L3 * LOAD_3
        temp = P_pv - real_load
        if temp > 0:
            p_bat = - temp if msg.bessSOC != 1 else 0.0

        if (p_bat + P_pv) > real_load and temp <= 0:
            p_bat = real_load - P_pv


    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Results message: ", L1, L2, L3, p_bat, panel)
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
