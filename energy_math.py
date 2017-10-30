"""This module contains mathematical functions needed to generate
data."""

__author__ = "Miroslav Nikolic and Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

from typing import Optional, Tuple
from random import random
from math import pi, cos

def vary(number: float) -> float:
    sign = -1 if random() <= 0.5 else 1
    # random number between 2 and 5 percent of starting number
    variation = (3 * random() + 2) * 0.01 * number
    return number + (variation * sign)

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
