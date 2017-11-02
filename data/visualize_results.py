import json
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import scipy.spatial as spatial

sample_rate = 60. # samples per hour

with open('results.json') as json_data:
    d = json.load(json_data)

overall = []
energyMark = []
performance = []
bessSOC = []
bessOverload = []
bessPower = []
mainGridPower = []
penal = []
current_load = []
solar_production = []
real_load = []
pv_power = []

for data_point in d:
    overall.append(data_point['overall'])
    energyMark.append(data_point['energyMark'])
    performance.append(data_point['performance'])
    bessSOC.append(data_point['bessSOC'])
    bessOverload.append(data_point['bessOverload'])
    bessPower.append(data_point['bessPower'])
    mainGridPower.append(data_point['mainGridPower'])
    penal.append(data_point['penal'])
    current_load.append(data_point['DataMessage']['current_load'])
    solar_production.append(data_point['DataMessage']['solar_production'])
    real_load.append(data_point['real_load'])
    pv_power.append(data_point['pv_power'])


t = np.arange(0., 24., 1./sample_rate)
 
fig, ax = plt.subplots(3, sharex=True)
ax[0].step(t, overall, picker=True)
ax[0].step(t, energyMark)
ax[0].step(t, performance)
ax[0].step(t, real_load)
ax[0].step(t, pv_power)
ax[0].set_title('Results')
ax[0].legend(['Overall', 'Energy mark', 'Performance', 'Real load', 'PV power'], loc = 'upper right', fontsize = 'small')
ax[1].step(t, bessSOC)
ax[1].step(t, bessOverload)
ax[1].legend(['BESS SOC', 'BESS overload'], loc = 'upper right', fontsize = 'small')
ax[2].step(t, bessPower)
ax[2].step(t, mainGridPower)
ax[2].step(t, current_load)
ax[2].step(t, solar_production)
ax[2].legend(['BESS power', 'Grid power', 'Total load', 'Solar power'], loc = 'upper right', fontsize = 'small')

plt.xlim(0, 24)

formatter = matplotlib.ticker.FuncFormatter(lambda m, x: time.strftime('%H:%M', time.gmtime(m*60*60)))
ax[2].xaxis.set_major_formatter(formatter)


plt.show()