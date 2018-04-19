# Python 3.6.1

import numpy as np
from itertools import product
import multiprocessing as mp

from raining_universe import RainingUniverse


def parallel_worker(rain_intensity, human_speed, save_path):
    ru = RainingUniverse()
    ru.save_path = save_path
    ru.universe_size = (200, 45, 40)
    ru.human_size = (175, 45, 20)
    ru.rain_intensity = rain_intensity
    ru.human_speed = human_speed
    ru.run_human_run()


Intensities = np.linspace(0.0, 1.0, 21).astype(float)
HumanSpeeds = np.linspace(200, 1200, 21)
Trials = np.arange(1, 6).astype(str)
ArgList = list(product(*(Intensities, HumanSpeeds, Trials)))
with mp.Pool() as Pool:
    Pool.starmap(parallel_worker, ArgList)

