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

If the result of the majority members prediction matching the actual game result, denote as 1 and vise versa.
 
For example: if there are 51% of group members voted that host will win the point spread gambling 
and the prediction was correct, denote the judgement result as 1.

| Column name | Type | Description | Example |
| :--- | :---: | :--- | :--- |
| game_id | string | Game unique id, which comes from date(YYYYmmDD) + game id of that date. | 20190526496 |
| national_point_spread_result | 0 or 1 | The prediction of the group member was correct with point spread gambling on national banker. | 1 |
 