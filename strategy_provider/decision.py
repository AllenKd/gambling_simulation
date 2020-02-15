class Decision:
    def __init__(self, game_type, game_date, gamble_id, decision):
        self.game_type = game_type
        self.game_date = game_date
        self.gamble_id = gamble_id
        self.decision = decision
        self.match = None

    def __str__(self):
        return 'type: %s, date: %s, id: %s' % self.game_type, self.game_date, self.gamble_id


# decision = {
#     "national": {
#         "over_threshold": [false, 1],
#         "spread_point": ["guest", 1]
#     },
#     "local": {
#         "over_threshold": [false, 0],
#         "spread_point": ["guest", 3],
#         "original": ["guest", 2]
#     }
# }
