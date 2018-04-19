# Python 3.6.1

import numpy as np


class RainingUniverse(object):
    def __init__(self):
        super().__init__()
        self._universe_size = tuple()  # 3-D; [0] -> height, [1] -> width, [2] -> length
        self.space0 = None
        self.sky_size = 0
        self.sky_shape = tuple()  # 2-D

        self._rain_speed = 93  # 93 dm/s; this speed is from online sources.
        self.rain_intensity = float()  # percentage of sky covered by rain
        self.rain_size = 0
        self.rain_space = None

        self._wind_speed = 0  # dm/s
        self.real_wind_speed = np.arange(1, self._rain_speed+1) / self._rain_speed * self.wind_speed

        self.human_size = tuple()  # 3-D, dimensionality consistent to self._size
        self.human_space = None
        self._human_speed = 10  # dm/s
        self.real_human_speed = np.arange(1, self._rain_speed+1) / self._rain_speed * self._human_speed
        self.real_human_speed = self.real_human_speed.astype(int)

        self.wetness = 0

    @property
    def universe_size(self):
        return self._universe_size

    @universe_size.setter
    def universe_size(self, a_tuple):
        self._universe_size = a_tuple
        self.space0 = np.zeros(a_tuple)
        self.sky_size = self._universe_size[1] * self._universe_size[2]
        self.sky_shape = (self._universe_size[1], self._universe_size[2])
        self.rain_space = np.zeros(a_tuple)

    @property
    def human_speed(self):
        return self._human_speed

    @human_speed.setter
    def human_speed(self, a_int):
        self._human_speed = a_int
        self.real_human_speed = np.arange(1, self._rain_speed+1) / self._rain_speed * self._human_speed
        self.real_human_speed = self.real_human_speed.astype(int)

    @property
    def wind_speed(self):
        return self._wind_speed

    @wind_speed.setter
    def wind_speed(self, a_int):
        self._wind_speed = a_int
        self.real_wind_speed = np.arange(1, self._rain_speed+1) / self._rain_speed * self._wind_speed
        self.real_wind_speed = self.real_wind_speed.astype(int)

    @property
    def rain_speed(self):
        return self._rain_speed

    @rain_speed.setter
    def rain_speed(self, a_int):
        self._rain_speed = a_int
        self.real_human_speed = np.arange(1, self._rain_speed+1) / self._rain_speed * self._human_speed
        self.real_human_speed = self.real_human_speed.astype(int)
        self.real_wind_speed = np.arange(1, self._rain_speed+1) / self._rain_speed * self._wind_speed
        self.real_wind_speed = self.real_wind_speed.astype(int)

    def checksum(self):
        if self.rain_intensity > 1. or self.rain_intensity < 0.:
            raise Exception('rain_intensity should be in range [0.0, 1.0]!')
        if any(np.array(self.human_size) - np.array(self._universe_size) > 0):
            raise Exception('human_size cannot be larger than universe_size in any dimension!')

    def generate_raindrops(self):
        self.rain_size = int(self.rain_intensity * self.sky_size)
        self.rain_space[0] = np.random.permutation(
            np.append(np.ones(self.rain_size), np.zeros(self.sky_size - self.rain_size))
        ).reshape(self.sky_shape)

    def update_raindrops(self):
        self.rain_space = np.roll(self.rain_space, 1, axis=0)
        self.rain_space[0] = 0

    def blow(self, i):
        interval = self.real_wind_speed[0] if i == 0 else self.real_wind_speed[i] - self.real_wind_speed[i - 1]
        self.rain_space = np.roll(self.rain_space, interval, axis=2)

    def initialize_human(self):
        self.human_space = np.zeros(self._universe_size)
        self.human_space[self._universe_size[0]-self.human_size[0]:, :self.human_size[1], :self.human_size[2]] = 1
        self.get_wet()

    def update_human(self, i):
        interval = self.real_human_speed[0] if i == 0 else self.real_human_speed[i] - self.real_human_speed[i-1]
        self.human_space = np.roll(self.human_space, interval, axis=2)

    def get_wet(self):
        old_rain_space = self.rain_space
        self.rain_space = np.where(self.human_space.astype(bool), self.space0, self.rain_space)
        self.wetness += np.sum(old_rain_space - self.rain_space)

    def update_universe(self, human=True):
        for i in range(self.rain_speed):  # Every iteration is 1/self._rain_speed second
            if self.rain_space.any():
                self.update_raindrops()
                self.blow(i)
            if human:
                self.update_human(i)
                self.get_wet()
        self.generate_raindrops()

    def let_the_rain_drop(self):
        time = int(self._universe_size[0] / self._rain_speed) + 1
        for i in range(time):
            print('Initializing the rain, %s/%s seconds' % (i+1, time))
            self.update_universe(human=False)

    def run_human_run(self):
        self.checksum()
        self.let_the_rain_drop()
        self.initialize_human()
        time = int((self._universe_size[2] - self.human_size[2]) / self.human_speed)
        for i in range(time):
            print('Simulating time %s of %s (seconds)' % (i+1, time))
            self.update_universe()
