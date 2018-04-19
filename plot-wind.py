# Python 3.6.1

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


WindSpeeds_list = list()
HumanSpeeds_list = list()
Wetness_list = list()
ResultList = np.arange(1, 6).astype(str)

for ResultPath in ResultList:
    WindSpeeds = list()
    HumanSpeeds = list()
    Wetness = list()
    with open('./wind_results0.6/' + ResultPath, 'r') as Result:
        for line in Result:
            line = line.split()
            WindSpeeds.append(float(line[0]))
            HumanSpeeds.append(float(line[1]))
            Wetness.append(float(line[2]))
    WindSpeeds_list.append(WindSpeeds)
    HumanSpeeds_list.append(HumanSpeeds)
    Wetness_list.append(Wetness)

WindSpeeds_list = np.average(np.array(WindSpeeds_list), axis=0).reshape((41, 41))
HumanSpeeds_list = np.average(np.array(HumanSpeeds_list), axis=0).reshape((41, 41))
Wetness_list = np.average(np.array(Wetness_list), axis=0).reshape((41, 41))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(HumanSpeeds_list, WindSpeeds_list, Wetness_list, cmap='jet')
ax.plot_surface(WindSpeeds_list, HumanSpeeds_list, Wetness_list, cmap='jet')
# ax.auto_scale_xyz([20, 100], [-10, 10], [0])
ax.set_ylabel('Human Speed (dm/s)')
ax.set_xlabel('Wind Speed (dm/s)')
ax.set_zlabel('Wetness (drops caught)')
plt.title('Intensity = 0.6')
plt.savefig('wind0.6-2.jpg')
