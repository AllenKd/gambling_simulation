class GambleInfo:
    def __init__(self, gamble_info):
        self.game_id = gamble_info['game_id']
        self.game_time = gamble_info['game_time']
        self.game_type = gamble_info['game_type']
        self.guest = gamble_info['guest']['name']
        self.host = gamble_info['host']['name']
        self.handicap = gamble_info['gamble_info']
        self.prediction = gamble_info['prediction']


class GambleResult:
    def __init__(self, gamble_info):
        self.game_id = gamble_info['game_id']
        self.game_time = gamble_info['game_time']
        self.game_type = gamble_info['game_type']
        self.guest = gamble_info['guest']
        self.host = gamble_info['host']
        self.judgement = gamble_info['judgement']