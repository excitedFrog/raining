# Python 3.6.1

import numpy as np


# Think about reality when assign the sizes and speeds, or you can get funny results if that pleases you.
# TODO: Add wind (shouldn't be difficult)
class RainingUniverse(object):
    def __init__(self):
        super().__init__()
        self.rd_process = 50

        self._universe_size = tuple()  # 3-D; [0] -> height, [1] -> width, [2] -> length
        self.space0 = None
        self.sky_size = 0
        self.sky_shape = tuple()  # 2-D

        self._rain_speed = 930  # 930 cm/s; this speed is from online sources.
        self.rain_intensity = float()  # percentage of sky covered by rain
        self.rain_size = 0
        self.rain_space = None

        self.human_size = tuple()  # 3-D, dimensionality consistent to self._size
        self.human_space = None
        self._human_speed = 100  # cm/s
        self.real_human_speed = np.arange(1, self._rain_speed+1) / self._rain_speed * self._human_speed
        self.real_human_speed = self.real_human_speed.astype(int)

        self.wetness = 0
        self.save_path = 'result'

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
    def rain_speed(self):
        return self._rain_speed

    @rain_speed.setter
    def rain_speed(self, a_int):
        self._rain_speed = a_int
        self.real_human_speed = np.arange(1, self._rain_speed+1) / self._rain_speed * self._human_speed
        self.real_human_speed = self.real_human_speed.astype(int)

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
            if (i + 1) % self.rd_process == 0:
                print('Rain dropping, frame %s of %s' % (i+1, self._rain_speed))
                print(self.wetness)
            if self.rain_space.any():
                self.update_raindrops()
            if human:
                self.get_wet()
                self.update_human(i)
                self.get_wet()
        self.generate_raindrops()

    def let_the_rain_drop(self):
        time = int(self._universe_size[0] / self._rain_speed) + 1
        for i in range(time):
            print('Initializing the rain, %s/%s seconds' % (i+1, time))
            self.update_universe(human=False)

    def save_results(self):
        with open(self.save_path, 'a') as save:
            save.write('%.3f %s %s\n' % (self.rain_intensity, self.human_speed, self.wetness))

    def run_human_run(self):
        self.checksum()
        self.let_the_rain_drop()
        self.initialize_human()
        time = int(self._universe_size[2] - self.human_size[2] / self.human_speed)
        for i in range(time):
            print('Simulating time %s of %s (seconds)' % (i+1, time))
            self.update_universe()
        self.save_results()


# 3-D; [0] -> height, [1] -> width, [2] -> length
if __name__ == '__main__':
    RU = RainingUniverse()
    RU.rain_intensity = 0.2
    RU.human_speed = 100
    RU.universe_size = (200, 45, 40)
    RU.human_size = (175, 45, 20)
    RU.run_human_run()
