from collections import defaultdict

game_id = 'game_id'
percentage_national_point_spread_guest = 'percentage_national_point_spread_guest'
percentage_national_point_spread_host = 'percentage_national_point_spread_host'
population_national_point_spread_guest = 'population_national_point_spread_guest'
population_national_point_spread_host = 'population_national_point_spread_host'
play_time = 'play_time'
host_id = 'host_id'
guest_id = 'guest_id'
host_score = 'host_score'
guest_score = 'guest_score'
national_host_point_spread = 'host_point_spread'
win_if_meet_spread_point = 'win_if_meet_spread_point'
response_if_meet_spread_point = 'response_if_hit_spread_point'
national_total_point = 'national_total_point'
local_host_point_spread = 'local_host_point_spread'
local_total_point_threshold = 'local_host_total_point'
local_host_point_spread_response_ratio = 'local_host_point_spread_response_ratio'
local_total_point_threshold_response_ratio = 'local_total_point_threshold_response_ratio'
local_origin_guest_response_ratio = 'local_origin_guest_response_ratio'
local_origin_host_response_ratio = 'local_origin_host_response_ratio'
guest = 'guest'
host = 'host'

chinese_mapping = {'客': 'guest', '主': 'host', '贏': True, '輸': False}
team_name_mapping = {'密爾瓦基公鹿': 'MIL',
                     '亞特蘭大老鷹': 'ATL',
                     '達拉斯獨行俠': 'DAL',
                     '洛杉磯湖人': 'LAL',
                     '紐奧良鵜鶘': 'NO',
                     '沙加緬度國王': 'SAC',
                     '聖安東尼奧馬刺': 'SA',
                     '華盛頓巫師': 'WAS',
                     '丹佛金塊': 'DEN',
                     '夏洛特黃蜂': 'CHA',
                     '金州勇士': 'GS',
                     '曼斐斯灰熊': 'MEM',
                     '洛杉磯快艇': 'LAC',
                     '奧克拉荷馬雷霆': 'OKC',
                     '底特律活塞': 'DET'}

default_prediction_table = defaultdict(list).fromkeys((game_id,
                                                       percentage_national_point_spread_guest,
                                                       percentage_national_point_spread_host,
                                                       population_national_point_spread_guest,
                                                       population_national_point_spread_host))

default_game_info_table = defaultdict(list).fromkeys((game_id,
                                                      play_time,
                                                      host_id,
                                                      guest_id,
                                                      host_score,
                                                      guest_score,
                                                      national_host_point_spread,
                                                      win_if_meet_spread_point,
                                                      response_if_meet_spread_point,
                                                      national_total_point,
                                                      local_host_point_spread,
                                                      local_host_point_spread_response_ratio,
                                                      local_total_point_threshold,
                                                      local_total_point_threshold_response_ratio,
                                                      local_origin_guest_response_ratio,
                                                      local_origin_host_response_ratio))
