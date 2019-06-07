# Simulator

Create multiple [Player](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/player) 
instances and a [Banker](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/banker) 
to simulate gambling scenario.

## Parameter

| Parameter | type | Description | Example |
| :---: | :---: | :--- | :---: |
| play_times | int | Number of gambling times. | 100 |
| number_of_player | int | Number of Player instance to create. | 100 |
| player_init_money | int | Total money of each Player at beginning. | 10000 |
| combination | int | Game combination, if combination is n, the win condition is all of these n games are won. <br> i.e. win_probability_of_each_game = 1/2^n | 1 |
| player_put_strategy | list of string | Put strategy for each Player, the list size should be equal to "number_of_player". | ['linear_response', 'linear_response', 'foo_double', 'kelly'] |
| player_bet_strategy | list of string | Bet strategy for each Player, the list size should be equal to "number_of_player". | ['random', 'keep_false', 'follow_last', 'random] | |
| to_db | bool | Write the simulation result into DB or not. | True |
