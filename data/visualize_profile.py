import json
import matplotlib.pyplot as plt
import numpy as np

sample_rate = 60. # samples per hour

with open('test_profiles_dm1.json') as json_data:
    d = json.load(json_data)

gridStatus = []
buyingPrice = []
sellingPrice = []
currentLoad = []
solarProduction = []
    
for data_point in d:
    gridStatus.append(data_point['gridStatus'])
    buyingPrice.append(data_point['buyingPrice'])
    sellingPrice.append(data_point['sellingPrice'])
    currentLoad.append(data_point['currentLoad'])
    solarProduction.append(data_point['solarProduction'])
    

t = np.arange(0., 24., 1./sample_rate)
 
fig, ax = plt.subplots(3, sharex=True)
ax[0].step(t,gridStatus)
ax[0].set_title('Profiles')
ax[0].legend(['Grid status'], loc = 'upper right', fontsize = 'small')
ax[0].set_ylim(-0.1,1.1)
ax[1].step(t,buyingPrice)
ax[1].step(t,sellingPrice)
ax[1].legend(['Buying price', 'Selling price'], loc = 'upper right', fontsize = 'small')
ax[2].step(t,currentLoad)
ax[2].step(t,solarProduction)
ax[2].legend(['Total load', 'Solar production'], loc = 'upper right', fontsize = 'small')

plt.xlim(0, 24)

 
# plt.subplot(211) 
# plt.plot(t,gridStatus)
# plt.xlim(0, 24)
# #plt.xticks(np.arange(0., 24., 4.))
# plt.xlabel('Grid status')

# plt.subplot(212)
# plt.plot(t,buyingPrice)
# plt.xlabel('Buying price')

plt.show()