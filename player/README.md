# Player

An instance to battle with the banker, as normal gambling rule,
put money and bet a result first, if the result is the same as the banker,
the player won this game and get the price equal to put_money times feedback_ratio.

## Parameter

| Parameter | type | Description | Example |
| :---: | :---: | :--- | :---: |
| player_id | int | Player unique identification. | 1 |
| play_times | int | Times of the player to gamble with the [Banker](Banker), stop earlier if the Player bankrupted. | 10 |
| strategy_provider | [StrategyProvider](StrategyProvider) | To provide a strategy table about bet for player reference. | [StrategyProvider](StrategyProvider) |
| combination | int | Game combination, if combination is n, the win condition is all of these n games are won. <br> i.e. win_probability_of_each_game = 1/2^n | 1 |
| money | int | Initial money of the Player. | 5000 |
| put_strategy | string | Strategy about the volume of bet to put, which obtain from [StrategyProvider](StrategyProvider), usually a table. | 'linear_response' |
| bet_strategy | string | Strategy about how to determine the result of the next game. | 'random' |
| bet_data | list | Predictions of games, the size equal to play_times | \[0, 1, 0, 1, 0, 1, 0, 1, 0, 1\] |

currently is just some foo strategy, and the win ration technically is 1 / 2^combination, **but it will based on deep learning to improve win ratio**, and it's the key value of this project

# Strategy Provider

An instance to calculate and generate strategy tables,
the strategy table used for Player instance to reference about
how much of money should put at next game,
the volume according to strategy and the times of continuous lose.

## Strategy Table Column Description

| Column name | Description |
| :--- | :--- |
| Continuous lose count | Number of lost game continuously. |
| Expected win unit | Expected win unit. |
| Current put unit | Recommendation unit to put when lose games for n times continuously. |
| Accumulative put unit | Accumulative put unit (include current run). |
| Win response unit | Response unit if current run won, the value will be "Current put unit" times 1.75(default odds). |
| Subtotal unit | Per-run summarized, the value will be "Win response unit" minus "Accumulative put unit". |

## Strategies

### linear response

The concept of this strategy is focus on the result of current money,
it calculate how much of bet for this run can be ont only cover past lost,
but also the final result will be the same as win for each run with minimum bet.

Strategy table:

| Continuous lose count | Expected win unit | Current put unit | Accumulative put unit | Win response unit | Subtotal unit |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | 0.75 | 1 | 1 | 1.75 | 0.75 |
| 1 | 1.50 | 4 | 5 | 7.00 | 2.00 |
| 2 | 2.25 | 10 | 15 | 17.50 | 2.50 |
| 3 | 3.00 | 24 | 39 | 42.00 | 3.00 |
| 4 | 3.75 | 57 | 96 | 99.75 | 3.75 |
| 5 | 4.50 | 134 | 230 | 234.50 | 4.50 |
| 6 | 5.25 | 314 | 544 | 549.50 | 5.50 |
| 7 | 6.00 | 734 | 1278 | 1284.50 | 6.50 |
| 8 | 6.75 | 1713 | 2991 | 2997.75 | 6.75 |
| 9 | 7.50 | 3998 | 6989 | 6996.50 | 7.50 |
| ... | ... | ... | ... | ... | ... |

### fibonacci base

As the name implies, the bet will increasing along with continuous lose based on
fibonacci series.

Strategy table:

| Continuous lose count | Expected win unit | Current put unit | Accumulative put unit | Win response unit | Subtotal unit |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | N/A | 1 | 1 | 1.75 | 0.75 |
| 1 | N/A | 1 | 2 | 1.75 | -0.25 |
| 2 | N/A | 2 | 4 | 3.50 | -0.50 |
| 3 | N/A | 3 | 7 | 5.25 | -1.75 |
| 4 | N/A | 5 | 12 | 8.75 | -3.25 |
| 5 | N/A | 8 | 20 | 14.00 | -6.00 |
| 6 | N/A | 13 | 33 | 22.75 | -10.25 |
| 7 | N/A | 21 | 54 | 36.75 | -17.25 |
| 8 | N/A | 34 | 88 | 59.50 | -28.50 |
| 9 | N/A | 55 | 143 | 96.25 | -46.75 |
| ... | ... | ... | ... | ... | ... |

### foo double

Put double bet of last run if lose, otherwise put minimum bet.

Strategy table:

| Continuous lose count | Expected win unit | Current put unit | Accumulative put unit | Win response unit | Subtotal unit |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | N/A | 1 | 1 | 1.75 | 0.75 |
| 1 | N/A | 2 | 3 | 3.50 | 0.50 |
| 2 | N/A | 4 | 7 | 7.00 | 0.00 |
| 3 | N/A | 8 | 15 | 14.00 | -1.00 |
| 4 | N/A | 16 | 31 | 28.00 | -3.00 |
| 5 | N/A | 32 | 63 | 56.00 | -7.00 |
| 6 | N/A | 64 | 127 | 112.00 | -15.00 |
| 7 | N/A | 128 | 255 | 224.00 | -31.00 |
| 8 | N/A | 256 | 511 | 448.00 | -63.00 |
| 9 | N/A | 512 | 1023 | 896.00 | -127.00 |
| ... | ... | ... | ... | ... | ... |

### kelly

Put based on [Kelly formula](https://en.wikipedia.org/wiki/Kelly_criterion), 
there is no strategy table because of how much to put is based on current residual money, 
and the residual money based on the result of each gambling, which is undetermined.
