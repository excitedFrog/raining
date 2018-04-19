# Python 3.6.1

import sys
import numpy as np
from itertools import product
import multiprocessing as mp

from raining_universe import RainingUniverse

RESULT_DIR = './wind_results/'
RESULT_PATH = sys.argv[1] if len(sys.argv) > 1 else '4'


def parallel_worker(wind_speed, human_speed):
    ru = RainingUniverse()
    ru.universe_size = (20, 4, 200)
    ru.human_size = (18, 4, 2)
    ru.rain_intensity = 0.6
    ru.wind_speed = wind_speed
    ru.human_speed = human_speed
    ru.run_human_run()
    return ru.wind_speed, ru.human_speed, ru.wetness


WindSpeeds = np.linspace(-100, 100, 41)
HumanSpeeds = np.linspace(10, 100, 41)
ArgList = list(product(*(WindSpeeds, HumanSpeeds)))
with mp.Pool() as Pool:
    Results = Pool.starmap(parallel_worker, ArgList)
with open(RESULT_DIR + RESULT_PATH, 'w') as SaveFile:
    for Item in Results:
        SaveFile.write(' '.join(list(map(str, Item))) + '\n')
