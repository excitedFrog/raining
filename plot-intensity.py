# Python 3.6.1

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


Intensities_List = list()
HumanSpeeds_list = list()
Wetness_list = list()
ResultList = np.arange(1, 6).astype(str)

for ResultPath in ResultList:
    Intensities = list()
    HumanSpeeds = list()
    Wetness = list()
    with open('./intensity_results/' + ResultPath, 'r') as Result:
        for line in Result:
            line = line.split()
            Intensities.append(float(line[0]))
            HumanSpeeds.append(float(line[1]))
            Wetness.append(float(line[2]))
    Intensities_List.append(Intensities)
    HumanSpeeds_list.append(HumanSpeeds)
    Wetness_list.append(Wetness)

Intensities_List = np.average(np.array(Intensities_List), axis=0).reshape((41, 41))
HumanSpeeds_list = np.average(np.array(HumanSpeeds_list), axis=0).reshape((41, 41))
Wetness_list = np.average(np.array(Wetness_list), axis=0).reshape((41, 41))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.auto_scale_xyz([10, 100], [0.0, 1.0], [0])
ax.set_xlabel('Human Speed (dm/s)')
ax.set_ylabel('Rain Intensity')
ax.set_zlabel('Wetness (drops caught)')
ax.plot_surface(HumanSpeeds_list, Intensities_List, Wetness_list, cmap='jet')
plt.savefig('intensity.jpg')
