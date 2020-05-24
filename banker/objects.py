from datetime import datetime

from config.logger import get_logger


class GambleInfo:
    def __init__(self, gamble_info):
        self.logger = get_logger(self.__class__.__name__)
        self.gamble_id = gamble_info.get("gamble_id", -1)
        self.game_time = gamble_info["game_time"]
        self.game_date = str(
            datetime.strptime(self.game_time[:10], "%Y-%m-%d").date().strftime("%Y%m%d")
        )
        self.game_type = gamble_info["game_type"]
        self.guest = gamble_info["guest"]["name"]
        self.host = gamble_info["host"]["name"]
        self.handicap = gamble_info["gamble_info"]
        self.prediction = gamble_info["prediction"]
        self.filter_out_invalid_gamble()

    def __str__(self):
        return f"gamble_id: {self.gamble_id}, type: {self.game_type}, date: {self.game_date}"

    def filter_out_invalid_gamble(self):
        self.logger.debug(f"filtering invalid gamble: {self.handicap}")
        for banker_side, gamble_types in self.handicap.items():
            for gamble_type in list(gamble_types):
                if "response" not in gamble_types[gamble_type]:
                    self.delete_gamble(banker_side, gamble_type)

                elif 0.0 in gamble_types[gamble_type]["response"].values():
                    self.delete_gamble(banker_side, gamble_type)

        self.logger.debug(f"filtered handicap: {self.handicap}")

    def delete_gamble(self, banker_side, gamble_type):
        self.logger.debug(f"invalid gamble type: {gamble_type}, delete it")
        del self.handicap[banker_side][gamble_type]
        for p in self.prediction:
            del p[banker_side][gamble_type]

    def is_valid(self, banker_side, game_type):
        self.logger.debug(f"check game validation, banker side: {banker_side}, game type: {game_type}")
        try:
            response_info = self.handicap[banker_side][game_type]['response']
            return len(response_info) == 2 and 0 not in response_info.values()
        except KeyError:
            self.logger.info(f"invalid game, banker side: {banker_side}, game type: {game_type}, gamble info: {self}")
            return False


class GambleResult:
    def __init__(self, gamble_info):
        self.gamble_id = gamble_info["gamble_id"]
        self.game_time = gamble_info["game_time"]
        self.game_type = gamble_info["game_type"]
        self.guest = gamble_info["guest"]
        self.host = gamble_info["host"]
        self.judgement = gamble_info["judgement"]["game"]
