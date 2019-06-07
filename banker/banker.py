import numpy as np


class Banker(object):
    def __init__(self, play_times, combination=1):
        self.game_result = np.random.randint(2, size=play_times * combination).reshape(play_times, combination)
        # TODO: add option to get game_result from DB
