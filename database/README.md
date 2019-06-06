# Database

Record all competition data comes from [Crawler]() and [Analyzer]()

## Table Description

Tables can be classify into some classes.

### Source Data

Obtain from web directly without additional logic.

#### game_data

Record original data about competition and gambling information.

| Column name | Type | Description | Example |
| :--- | :---: | :--- | :--- |
| game_id | string | Game unique id, which comes from date(YYYYmmDD) + game id of that date. | 20190526496 |
| play_time | string | Game start time. | 08:30 |
| AM_PM | string | Game start on AM or PM. | AM |
| guest | string | Abbreviation of guest team. | MIL |
| host | string | Abbreviation of host team. | TOR |
| guest_score | int | Final score that guest team got in this game. | 94 |
| host_score | int | Final score that guest team got in this game. | 100 |
| national_total_point_threshold | int | Total point gambling of national banker. | 218 |
| national_host_point_spread | int | Point spread gambling of national banker in host view. | 8 |
| win_if_meet_spread_point | 0 or 1 | Win or lose partial of money if the result after point spread was tie. | 1 |
| response_ratio_if_hit_spread_point | float | Response ratio if the result after point spread was tie. | 1.5 |
| local_host_point_spread | float | Point spread gambling of Taiwan banker in host view. | 6.5 |
| local_host_point_spread_response_ratio | float | Response ratio of point spread gambling in Taiwan. | 1.8 |
| local_total_point_threshold | float | Total point gambling of Taiwan banker. | 218.5 |
| local_total_point_threshold_response_ratio | float | Response ratio if won the total point gambling in Taiwan. | 1.8 |
| local_origin_guest_response_ratio | float | Response ratio of guest win without point spread. | 2.7 |
| local_origin_host_response_ratio | float | Response ratio of host win without point spread. | 1.28 |

#### prediction_data

Record predictions from members, those members been classified into 4 groups, 
* all member: all members.
* all_prefer: all member with highly confident.
* more_than_sixty: members with more 60% hit ratio.
* top_100: top 100 members.

| Column name | Type | Description | Example |
| :--- | :---: | :--- | :--- |
| game_id | string | Game unique id, which comes from date(YYYYmmDD) + game id of that date. | 20190526496 |
| percentage_national_point_spread_guest | int | Percentage of the member group vote guest with point spread gambling on national banker. | 49 |
| population_national_point_spread_guest | int | Population of the member group vote guest with point spread gambling on national banker. | 885 |
| percentage_national_point_spread_host | int | Percentage of the member group vote host with point spread gambling on national banker. | 51 |
| population_national_point_spread_host | int | Population of the member group vote host with point spread gambling on national banker. | 935 |
| percentage_national_total_point_over | int | Percentage of the member group vote over with total score gambling on national banker. | 45 |
| population_national_total_point_over | int | Population of the member group vote over with total score gambling on national banker. | 436 |
| percentage_national_total_point_under | int | Percentage of the member group vote under with total score gambling on national banker. | 55 |
| population_national_total_point_under | int | Population of the member group vote under with total score gambling on national banker. | 529 |
| percentage_local_point_spread_guest | int | Percentage of the member group vote guest with point spread gambling on local banker. | 45 |
| population_local_point_spread_guest | int | Population of the member group vote guest with point spread gambling on local banker. | 763 |
| percentage_local_point_spread_host | int | Percentage of the member group vote host with point spread gambling on local banker. | 55 |
| population_local_point_spread_host | int | Population of the member group vote host with point spread gambling on local banker. | 919 |
| percentage_local_total_point_over | int | Percentage of the member group vote over with total score gambling on Taiwan banker. | 44 |
| population_local_total_point_over | int | Population of the member group vote over with total score gambling on Taiwan banker. | 411 |
| percentage_local_total_point_under | int | Percentage of the member group vote under with total score gambling on Taiwan banker. | 56 |
| population_local_total_point_under | int | Population of the member group vote under with total score gambling on Taiwan banker. | 526 |
| percentage_local_original_guest | int | Percentage of the member group vote guest without point spread gambling on local banker. | 18 |
| population_local_original_guest | int | Population of the member group vote guest without point spread gambling on local banker. | 101 |
| percentage_local_original_host | int | Percentage of the member group vote host without point spread gambling on local banker. | 82 |
| population_local_original_host | int | Population of the member group vote host without point spread gambling on local banker. | 451 |

### Judgement Data

Record judgements about the games and members predictions.

#### game_judgement

Record gambling result.

| Column name | Type | Description | Example |
| :--- | :---: | :--- | :--- |
| game_id | string | Game unique id, which comes from date(YYYYmmDD) + game id of that date. | 20190526496 |
| host_win_original | 0 or 1 | The host won the game originally. | 1 |
| host_win_point_spread_national | 0 or 1 | The host won the game with point spread gambling on national banker. | 1 |
| host_win_point_spread_local | 0 or 1 | The host won the game with point spread gambling on Taiwan banker. | 1 |
| over_total_point_national | 0 or 1 | The total score was over the threshold with total score gambling on national banker. | 1 |
| over_total_point_local | 0 or 1 | The total score was over the threshold with total score gambling on Taiwan banker. | 1 |  
   
#### prediction_judgement

Record judgements of predictions from members, those members been classified into 4 groups also, 
* all member: all members.
* all_prefer: all member with highly confident.
* more_than_sixty: members with more 60% hit ratio.
* top_100: top 100 members.

If the result of the majority members' prediction matching the actual game result, denote as 1 and vise versa.
 
For example: if there are 51% of group members voted that host will win the point spread gambling 
and the prediction was correct, denote the judgement result as 1.

| Column name | Type | Description | Example |
| :--- | :---: | :--- | :--- |
| game_id | string | Game unique id, which comes from date(YYYYmmDD) + game id of that date. | 20190526496 |
| national_point_spread_result | 0 or 1 | The prediction of the group member was correct with point spread gambling on national banker. | 1 |
| national_point_spread_percentage | int | Percentage of win members of the group in point spread gambling with national banker. | 51 |
| national_point_spread_population | int | Population of win members of the group in point spread gambling with national banker. | 935 |
| national_total_point_result | 0 or 1 | The prediction of the group member was correct with total score gambling on national banker. | 0 |
| national_total_point_percentage | int | Percentage of win members of the group in total score gambling with national banker. | 45 |
| national_total_point_population | int | Population of win members of the group in total score gambling with national banker. | 436 |
| local_point_spread_result | 0 or 1 | The prediction of the group member was correct with point spread gambling on local banker. | 1 |
| local_point_spread_percentage | int | Percentage of win members of the group in point spread gambling with local banker. | 55 |
| local_point_spread_population | int | Population of win members of the group in point spread gambling with local banker. | 919 |
| local_total_point_result | 0 or 1 | The prediction of the group member was correct with total score gambling on local banker. | 0 |
| local_total_point_percentage | int | Percentage of win members of the group in total score gambling with local banker. | 44 |
| local_total_point_population | int | Population of win members of the group in total score gambling with local banker. | 411 |
| local_original_result | 0 or 1 | The prediction of the group member was correct with original score gambling on local banker. | 1 |
| local_original_percentage | int | Percentage of win members of the group in original score gambling with local banker. | 82 |
| local_original_population | int | Population of win members of the group in original score gambling with local banker. | 451 |

### Simulated Data

The simulator can simulate a banker and multiple players to battle with it, 
and the detail would be by-player recorded.

#### player_n

Each player own a table to record battle detail, the table name followed by player id, 
for example, the first player with player_id=1 would use the table "player_1".

| Column name | Type | Description | Example |
| :--- | :---: | :--- | :--- |
| run | int | The nth time of gambling, start from 0. | 0 |
| current_put | int | Bet of this run. | 100 |
| win_result | 0 or 1 | Win or lose at this run. | 1 |
| current_response | int | Money to get back, the value would be current_put times odds if win, else 0. | 175 |
| subtotal | int | Current total money. | 10075 |
| actual_win | int | Net profit. | 75 |
| expected_win | int | Set to average odds times minimum bets for every day, so the value would be increasing linearly along with the number of run. | 75 | 
 
### Summarized Data
 
Summarized result of prediction judgement and simulation.
* all member: all members.
* all_prefer: all member with highly confident.
* more_than_sixty: members with more 60% hit ratio.
* top_100: top 100 members.
 
#### prediction_judgement_summarize
 
Record summarized data by each group.
 
| Column name | Type | Description | Example |
| :--- | :---: | :--- | :--- |
| member_group | string | Member group, which will be one of member groups as prediction judgement. | all_member |
| national_point_spread_win_ration | float | The win ratio on point spread gambling with national banker. | 0.498971 |
| national_point_spread_max_continuous_lose | int | Max count of continuously lose of point spread gambling with national banker. | 5 | 
| national_point_spread_number_of_valid_game | int | Number of record of point spread gambling with national banker. | 123 |
| national_total_point_win_ration | float | The win ratio on total point gambling with national banker. | 0.498989 |
| national_total_point_max_continuous_lose | int | Max count of continuously lose of total point gambling with national banker. | 6 | 
| national_total_point_number_of_valid_game | int | Number of record of total point gambling with national banker. | 125 |
| local_point_spread_win_ration | float | The win ratio on point spread gambling with local banker. | 0.501020 |
| local_point_spread_max_continuous_lose | int | Max count of continuously lose of point spread gambling with local banker. | 5 | 
| local_point_spread_number_of_valid_game | int | Number of record of point spread gambling with local banker. | 124 |
| local_total_point_win_ration | float | The win ratio on total point gambling with local banker. | 0.501010 |
| local_total_point_max_continuous_lose | int | Max count of continuously lose of total point gambling with local banker. | 4 | 
| local_total_point_number_of_valid_game | int | Number of record of total point gambling with local banker. | 125 |
| local_original_win_ration | float | The win ratio on original gambling with local banker. | 0.501010 |
| local_original_max_continuous_lose | int | Max count of continuously lose of original gambling with local banker. | 4 | 
| local_original_number_of_valid_game | int | Number of record of original gambling with local banker. | 125 |

#### player summarize

Record summarized data of each player.

| Column name | Type | Description | Example |
| :--- | :---: | :--- | :--- |
| player_id | int | Player id, which is serial number from 1. | 1 |
| put_strategy | string | The strategy the player used. | linear_response |
| initial_money | int | Player total money at beginning. | 10000 |
| still_survival | 0 or 1 | The player still have money after final gambling. | 1 |
| win_ratio | float | Win ratio during the whole gambling. | 0.49 | 
| max_continuous_lose_count | Max count od continuously lose. | 6 |
| final_money | int | Total money of the player after final gambling. | 8000 |
| final_result | 0 or 1 | Is final_money of the player more then the beginning or not. | 0 |
