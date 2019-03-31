from simulator import Simulator
from config import constant


def main():
    game_times = 100
    strategy_list = [constant.kelly, constant.linear_response, constant.fibonacci_base, constant.foo_double] * 10
    simulator = Simulator(play_times=game_times, number_of_player=len(strategy_list), player_init_money=300000,
                          to_db=True, player_strategy=strategy_list)
    simulator.start_simulation()


if __name__ == '__main__':
    main()
