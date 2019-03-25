from simulator import Simulator


def main():
    game_times = 1000
    strategy_list = ['kelly', 'linear_response', 'fibonacci_base', 'foo_double'] * 20
    simulator = Simulator(play_times=game_times, number_of_player=len(strategy_list), player_init_money=300000,
                          to_db=True, player_strategy=strategy_list)
    simulator.start_simulation()


if __name__ == '__main__':
    main()
