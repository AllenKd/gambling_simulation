

def test_simulator():
    from player import constant
    from simulator.simulator import Simulator
    game_times = 100
    strategy_list = [constant.kelly, constant.linear_response, constant.fibonacci_base, constant.foo_double] * 10
    simulator = Simulator(play_times=game_times, number_of_player=len(strategy_list), player_init_money=300000,
                          to_db=True, player_put_strategy=strategy_list, player_bet_strategy=constant.follow_last)
    simulator.start_simulation()


def test_create_db():
    from database.constructor import DbConstructor
    b = DbConstructor()
    b.create_schema(force=True)
    b.create_tables()


def test_crawler():
    from crawler.crawler import Crawler
    a = Crawler(start_date='20180929', end_date='20180930')
    a.start_crawler()


def test_analyzer():
    from analysis.crawled_result_analyzer import CrawledResultAnalyzer
    a = CrawledResultAnalyzer()
    a.start_analyzer()


if __name__ == '__main__':
    pass
    # test_create_db()
    test_crawler()
    # test_analyzer()
