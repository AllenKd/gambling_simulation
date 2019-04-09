from config import string_constant
from simulator import Simulator


def main():
    game_times = 100
    strategy_list = [string_constant.kelly, string_constant.linear_response, string_constant.fibonacci_base, string_constant.foo_double] * 10
    simulator = Simulator(play_times=game_times, number_of_player=len(strategy_list), player_init_money=300000,
                          to_db=True, player_put_strategy=strategy_list, player_bet_strategy=string_constant.follow_last)
    simulator.start_simulation()


if __name__ == '__main__':
    # main()
    from crawler.crawler import Crawler
    from database.constructor import DbConstructor
    b = DbConstructor()
    b.create_schema(force=True)
    b.create_tables()

    a = Crawler(start_date='20190215', end_date='20190218')
    a.start_crawler()
