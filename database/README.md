# Database

Record all competition data comes from [Crawler]

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

