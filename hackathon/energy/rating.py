"""This module handles rating of solution's returned messages."""

__author__ = "Miroslav Nikolic"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

from typing import Tuple
from hackathon.utils.utils import DataMessage, PVMode, ResultsMessage
import math

PENAL_L1 = 0
PENAL_L2 = 0
PENAL_L3 = 0
OVERLOADS = 0

def main_grid(on: bool,
              load_one: int,
              load_two: int,
              load_three: int,
              current_load: float,
              power_reference: float,
              solar_production: float,
              pv_mode: PVMode) -> float:
    s_prod = solar_production if pv_mode == PVMode.SUPPLY else 0
    factor = (load_one * 0.2 + load_two * 0.5 + load_three * 0.3) \
             * current_load
    if on:
        return factor - power_reference - s_prod
    else:
        return factor - s_prod

def energy_mark(consumption: float,
                penal: float,
                pv_sell: float,
                bess_sell: float) -> float:
    return consumption + penal - pv_sell - bess_sell

def get_physics_metrics(d: DataMessage, r: ResultsMessage,
                        spent_time: float, match: bool) \
                        -> Tuple[float, float, float, float,
                                 float, bool, float]:
    global OVERLOADS
    penal = 0.0
    if r.power_reference > 8:
        r.power_reference = 8
    elif r.power_reference < -8:
        r.power_reference = -8

    if (d.bessSOC == 0):
        r.power_reference = 0

    if not r.load_one and PENAL_L1 == 0:
        penal += 21
    elif not r.load_one and PENAL_L1 > 0:
        penal += 1

    if not r.load_two and PENAL_L2 == 0:
        penal += 4.4
    elif not r.load_two and PENAL_L2 > 0:
        penal += 0.4

    if not r.load_three and PENAL_L3 >= 0:
        penal += 0.1

    if d.grid_status and r.pv_mode == PVMode.SUPPLY:
        mg = main_grid(True, int(r.load_one), int(r.load_two),
                       int(r.load_three), d.current_load,
                       r.power_reference, d.solar_production, r.pv_mode)
        # we sell
        if mg < 0:
            bess_sell = abs(mg) * d.selling_price / 60
            consumption = 0.0
        else:
            consumption = mg * d.buying_price / 60
            bess_sell = 0

        current_power = r.power_reference

        soc_bess = d.bessSOC - r.power_reference / 600

        pv_sell = 0.0
        overload = False

    elif d.grid_status and r.pv_mode == PVMode.SELL:
        mg = main_grid(True, int(r.load_one), int(r.load_two),
                       int(r.load_three), d.current_load,
                       r.power_reference, d.solar_production, r.pv_mode)

        if mg < 0:
            bess_sell = abs(mg) * d.selling_price / 60
            consumption = 0.0
        else:
            consumption = (int(r.load_one) * 0.2 +
                           int(r.load_two) * 0.5 +
                           int(r.load_three) * 0.3) \
                           * d.current_load * d.buying_price / 60
            bess_sell = 0

        pv_sell = d.selling_price * d.solar_production / 60
        overload = False

        soc_bess = d.bessSOC - r.power_reference / 600

        current_power = r.power_reference

    elif d.grid_status and r.pv_mode == PVMode.OFF:
        mg = main_grid(True, int(r.load_one), int(r.load_two),
                       int(r.load_three), d.current_load,
                       r.power_reference, d.solar_production, r.pv_mode)

        if mg < 0:
            bess_sell = abs(mg) * d.selling_price / 60
            consumption = 0
        else:
            consumption = (int(r.load_one) * 0.2 +
                           int(r.load_two) * 0.5 +
                           int(r.load_three) * 0.3) \
                           * d.current_load * d.buying_price / 60
            bess_sell = 0

        pv_sell = 0
        overload = False

        soc_bess = d.bessSOC - r.power_reference / 600

        current_power = r.power_reference

    elif not d.grid_status:
        current_power = main_grid(False, int(r.load_one), int(r.load_two),
                                  int(r.load_three), d.current_load,
                                  r.power_reference, d.solar_production,
                                  r.pv_mode)

        if OVERLOADS >= 2 or (d.bessSOC == 0 and current_power > 0):
            penal = 25.5
            current_power = 0

        bess_sell = 0
        pv_sell = 0

        soc_bess = d.bessSOC - current_power / 600

        if current_power > 8:
            overload = True
            OVERLOADS += 1
        else:
            overload = False
            OVERLOADS = 0

        consumption = 0
        mg = 0

    if 0 > soc_bess:
        soc_bess = 0
    if soc_bess > 1:
        soc_bess = 1

    em = energy_mark(consumption, penal, pv_sell, bess_sell)
    return em, 1, mg, penal, soc_bess, overload, current_power
