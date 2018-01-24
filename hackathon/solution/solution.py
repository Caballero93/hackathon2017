"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir

global flag_solar
flag_solar = False

def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py
    # Dummy result is returned in every cycle here

    global flag_solar
    L1,L2,L3=True,True,True
    p_bat = 0.0
    panel=PVMode.ON
    if not msg.grid_status:
        temp=msg.solar_production+6-msg.current_load
        if temp<0:
            if temp>-0.3*msg.current_load:
                L3=False
            elif temp>-0.5*msg.current_load:
                L2 = False
            else:
                L2, L3 = False, False
        if msg.bessSOC < 0.56:
            L3=False
        if msg.bessSOC < 0.2:
            L2,L3=False,False
        if msg.solar_production>msg.current_load and msg.bessSOC>0.99:
            flag_solar = True
        if flag_solar:
            panel = PVMode.OFF

    else:
        flag_solar = False
        if msg.buying_price==3:
            if msg.bessSOC!=1:
                p_bat=-1.5
            else:
                p_bat=0.0
        else:
            p_bat = 4.0
            if msg.current_load > 6.5:
                L2 = False
            if msg.solar_production < 0.3*msg.current_load:
                L3=False
            LOAD_1 = 0.2 * msg.current_load
            LOAD_2 = 0.5 * msg.current_load
            LOAD_3 = 0.3 * msg.current_load
            real_load = LOAD_1 + int(L2) * LOAD_2 + int(L3) * LOAD_3
            temp = msg.solar_production - real_load
            if temp > 0:
                p_bat = -temp if msg.bessSOC != 1 else 0.0
            else:
                if p_bat + msg.solar_production > real_load:
                    p_bat = real_load - msg.solar_production

            # if msg.selling_price==0:
            #     if( temp > 0):
            #         p_bat=-temp
            #     else:
            #         if temp > -4.0:
            #             p_bat=-temp
            #         else:
            #             p_bat=4.0*msg.current_load/8
            # else:
            #     if(temp > 0):
            #         p_bat=0.0
            #     else:
            #         if temp > -4.0:
            #             p_bat=-temp
            #         else:
            #             p_bat=4.0*msg.current_load/8
                #p_bat=4.0



    if msg.bessSOC<0.2:
        if p_bat>0.0:
            p_bat=0.0


    return ResultsMessage(data_msg=msg,
                          load_one=L1,
                          load_two=L2,
                          load_three=L3,
                          power_reference =p_bat,
                          pv_mode=panel)


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
