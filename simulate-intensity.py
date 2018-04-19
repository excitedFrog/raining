# Python 3.6.1

import sys
import numpy as np
from itertools import product
import multiprocessing as mp

from raining_universe import RainingUniverse

RESULT_PATH = sys.argv[1] if len(sys.argv) > 1 else '5'


def parallel_worker(rain_intensity, human_speed):
    ru = RainingUniverse()
    ru.universe_size = (20, 4, 200)
    ru.human_size = (18, 4, 2)
    ru.wind_speed = 0
    ru.rain_intensity = rain_intensity
    ru.human_speed = human_speed
    ru.run_human_run()
    return ru.rain_intensity, ru.human_speed, ru.wetness


Intensities = np.linspace(0.0, 1.0, 41).astype(float)
HumanSpeeds = np.linspace(10, 100, 41)
ArgList = list(product(*(Intensities, HumanSpeeds)))
with mp.Pool() as Pool:
    Results = Pool.starmap(parallel_worker, ArgList)
with open(RESULT_PATH, 'w') as SaveFile:
    for Item in Results:
        SaveFile.write(' '.join(list(map(str, Item))) + '\n')
