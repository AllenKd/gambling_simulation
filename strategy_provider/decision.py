class Decision:
    def __init__(self, game_type, game_date, gamble_id, bets):
        self.game_type = game_type
        self.game_date = game_date
        self.gamble_id = gamble_id

        # list fo Bet object
        self.bets = bets
        self.match = None

    def __str__(self):
        return 'type: %s, date: %s, id: %s' % (self.game_type, self.game_date, self.gamble_id)


class Bet:
    def __init__(self, banker_side, bet_type, result, unit):
        self.banker_side = banker_side
        self.type = bet_type
        self.result = result
        self.unit = unit
