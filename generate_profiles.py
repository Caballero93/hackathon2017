from hackathon.energy.energy_math import gen_profile
from hackathon.utils.utils import *
import json

PROFILE_PREFIX = "./data/profiles"
LOAD_SCALES = [1.0, 1.1, 0.8, 1.2, 0.9]
SOLAR_SCALES = [1.3, 0.7, 0.8, 0.9, 1.1]
BLACKOUTS = [ [[11,11.5]], \
              [], \
              [], \
              [], \
              [], ]

profiles = []

# used to smoothen out the load profiles on day transitions
load_scaling_prev = 1.0

for i in CFG.days:
    n = i-1
    to_write, profile = gen_profile(CFG.sampleRate, load_scaling=LOAD_SCALES[n], load_scaling_prev=load_scaling_prev, solar_scaling=SOLAR_SCALES[n], blackouts=BLACKOUTS[n])
    profiles += profile
    load_scaling_prev = LOAD_SCALES[n]

with open(PROFILE_PREFIX + ".json", 'w') as f:
     f.write(json.dumps(profiles))





