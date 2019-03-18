import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class RandomGameGenerator(object):
    def __init__(self, times, combination=1):
        self.simulated_data = np.random.randint(2, size=times * combination).reshape(times, combination)

        # generate table
        shift_diff = np.all(self.simulated_data[1:] != self.simulated_data[:-1], axis=1)
        un_change_count = np.diff(np.flatnonzero(np.concatenate(([True], shift_diff, [True]))))
        unique, counts = np.unique(un_change_count, return_counts=True)
        counts_sum = np.cumsum(counts)
        counts_percentage = np.around(counts / sum(counts), decimals=5)
        counts_percentage_sum = np.cumsum(counts_percentage)
        idea = np.around(1 / (2 ** combination) ** unique, decimals=5)
        idea_sum = np.cumsum(idea)

        self.table = pd.DataFrame({'continuous': unique,
                                   'count': counts,
                                   'count_sum': counts_sum,
                                   'percentage': counts_percentage,
                                   'percentage_sum': counts_percentage_sum,
                                   'idea': idea,
                                   'idea_sum': idea_sum})


if __name__ == '__main__':
    game_time = 10000000
    a = RandomGameGenerator(game_time)
    a.table.plot()
    plt.show()
