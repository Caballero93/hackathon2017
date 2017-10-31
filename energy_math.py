"""This module contains mathematical functions needed to generate
data."""

__author__ = "Miroslav Nikolic and Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

import json
from random import random
from math import pi, cos
from functools import partial
from typing import Optional, Tuple

def buying_price(t: float) -> Optional[float]:
    if t < 7 or 23 <= t <= 24:
        return 2
    elif 7 <= t < 23:
        return 8
    else:
        raise Exception('Time should be between 0 and 24')

def selling_price(t: float) -> Optional[float]:
    if 0 <= t < 11 or 17 <= t <= 24:
        return 3
    elif 11 <= t < 17:
        return 0
    else:
        raise Exception('Time should be between 0 and 24')

def current_load(t: float) -> float:
    if 3 <= t < 13:
        return 5/2 * (cos(1/5 * pi * (t - 8)) + 1) + 3
    elif 13 <= t <= 24:
        return 6 * (cos(1/7 * pi * (t - 20)) + 1) + 3
    elif 0 <= t <3:
        return 6 * (cos(1/7 * pi * (t + 4)) + 1) + 3
    else:
        raise Exception('Time should be between 0 and 24')

def solar_produciton(t: float) -> float:
    if 7 <= t < 19:
        return 4 * (cos(1/6 * pi * (t - 13)) + 1)
    elif 0 <= t < 7 or 19 <= t <= 24:
        return 0
    else:
        raise Exception('Time should be between 0 and 24')

def grid_status(s: int) -> None:
    # TODO:
    data = []
    for s in range(s):
        data.append({'status': 1})

    return json.dumps(data)

def samples_to_time(samples_num: int, sample: int) -> float:
    """Converts sample number to day time."""
    return 24 / samples_num * sample

def gen_ideal(samples_num: int) -> str:
    """Generates ideal profile."""
    to_time = partial(samples_to_time, samples_num)
    data = []

    for s in range(samples_num):
        t = to_time(s)
        data.append({'buying_price': buying_price(t),
                     'selling_price': selling_price(t),
                     'current_load': current_load(t),
                     'solar_production': solar_produciton(t)})

    return json.dumps(data)
