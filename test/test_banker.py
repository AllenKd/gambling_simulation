import copy

import pytest

from banker.banker import Banker
from banker.objects import GambleInfo, GambleResult
from test.common import *
from util.util import Util


@pytest.fixture(scope="class")
def setup_test_data():
    mongo_client = Util.get_mongo_client()["gambling_simulation"]["sports_data"]
    mongo_client.insert_one(test_gamble_data)
    yield mongo_client
    mongo_client.delete_one(test_gamble_data)


class TestBanker:
    def test_get_gamble_info(self, setup_test_data):
        result = Banker().get_gamble_info("20181020", game_type="TEST")
        assert len(result) == 1
        assert (
            result[0].__dict__ == GambleInfo(copy.deepcopy(test_gamble_data)).__dict__
        )

    def test_get_gamble_result(self, setup_test_data):
        result = Banker()._get_gamble_result(game_date="20181020", gamble_id=-1)
        assert result.__dict__ == GambleResult(copy.deepcopy(test_gamble_data)).__dict__
