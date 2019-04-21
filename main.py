

def task_simulator():
    from player import constant
    from simulator.simulator import Simulator
    game_times = 100
    strategy_list = [constant.kelly, constant.linear_response, constant.fibonacci_base, constant.foo_double] * 10
    simulator = Simulator(play_times=game_times, number_of_player=len(strategy_list), player_init_money=300000,
                          to_db=True, player_put_strategy=strategy_list, player_bet_strategy=constant.follow_last)
    simulator.start_simulation()


def task_create_db():
    from database.constructor import DbConstructor
    b = DbConstructor()
    b.create_schema(force=True)
    b.create_tables()


def task_crawler():
    import datetime
    from crawler.crawler import Crawler
    a = Crawler(start_date='20180928', end_date=datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'))
    a.start_crawler()


def task_analyzer():
    from analysis.crawled_result_analyzer import CrawledResultAnalyzer
    a = CrawledResultAnalyzer(to_db=True)
    a.start_analyzer()


if __name__ == '__main__':
    task_create_db()
    task_crawler()
    task_analyzer()
