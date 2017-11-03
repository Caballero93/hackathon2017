from hackathon.energy.energy_math import gen_profile
from hackathon.utils.utils import *

PROFILE_PREFIX = "./data/profile_"
LOAD_SCALES = [1.0, 1.1, 0.8, 1.2, 0.9]
SOLAR_SCALES = [1.3, 0.7, 0.8, 0.9, 1.1]
BLACKOUTS = [ [[11,11.5]], \
              [], \
              [], \
              [], \
              [], ]

for i in range(len(LOAD_SCALES)):
    with open(PROFILE_PREFIX+str(i+1)+".json", 'w') as f:
        to_write, profile = gen_profile(CFG.samples_num, load_scaling=LOAD_SCALES[i], solar_scaling=SOLAR_SCALES[i], blackouts=BLACKOUTS[i])
        f.write(to_write)





