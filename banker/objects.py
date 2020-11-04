from datetime import datetime
import logging
from strategy_provider.common.decision import get_confidence


class GambleInfo:
    def __init__(self, gamble_info):
        self.gamble_id = gamble_info.get("gamble_id", -1)
        self.game_time = gamble_info["game_time"]
        self.game_date = str(
            datetime.strptime(self.game_time[:10], "%Y-%m-%d").date().strftime("%Y%m%d")
        )
        self.game_type = gamble_info["game_type"]
        self.guest = gamble_info["guest"]["name"]
        self.host = gamble_info["host"]["name"]

        self.gamble_info = {
            "total_point": self._parse_gamble_info(
                gamble_info["gamble_info"]["total_point"]
            ),
            "spread_point": self._parse_gamble_info(
                gamble_info["gamble_info"]["spread_point"]
            ),
            "original": self._parse_gamble_info(gamble_info["gamble_info"]["original"]),
        }

    def __str__(self):
        return f"gamble_id: {self.gamble_id}, type: {self.game_type}, date: {self.game_date}"

    def _parse_gamble_info(self, gamble_info):
        if self._is_valid(gamble_info):
            gamble_info["prediction"].pop("major")
            gamble_info["confidence"] = get_confidence(gamble_info["prediction"])
            return gamble_info
        return None

    @staticmethod
    def _is_valid(game):
        try:
            response_info = game["response"]
            return (
                len(response_info) == 2
                and all(response_info.values())
            )
        except KeyError:
            logging.info(f"no response info, invalid game: {game}")
            return False


class GambleResult:
    def __init__(self, gamble_info):
        self.gamble_id = gamble_info["gamble_id"]
        self.game_time = gamble_info["game_time"]
        self.game_type = gamble_info["game_type"]
        self.guest = gamble_info["guest"]
        self.host = gamble_info["host"]
        self.judgement = gamble_info["judgement"]["game"]
