# response_ratio = self.ratio_per_game if not response_ratio else response_ratio
#         bet_ratio = (win_prob * (response_ratio + 1) - 1) / response_ratio
#         return round(bet_ratio * chips, -2)