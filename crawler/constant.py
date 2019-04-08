from collections import defaultdict

# prediction
percentage_national_point_spread_guest = 'percentage_national_point_spread_guest'
percentage_national_point_spread_host = 'percentage_national_point_spread_host'
population_national_point_spread_guest = 'population_national_point_spread_guest'
population_national_point_spread_host = 'population_national_point_spread_host'

percentage_national_total_point_guest = 'percentage_national_total_point_guest'
percentage_national_total_point_host = 'percentage_national_total_point_host'
population_national_total_point_guest = 'population_national_total_point_guest'
population_national_total_point_host = 'population_national_total_point_host'

percentage_local_point_spread_guest = 'percentage_local_point_spread_guest'
percentage_local_point_spread_host = 'percentage_local_point_spread_host'
population_local_point_spread_guest = 'population_local_point_spread_guest'
population_local_point_spread_host = 'population_local_point_spread_host'

percentage_local_total_point_guest = 'percentage_local_total_point_guest'
percentage_local_total_point_host = 'percentage_local_total_point_host'
population_local_total_point_guest = 'population_local_total_point_guest'
population_local_total_point_host = 'population_local_total_point_host'

percentage_local_original_guest = 'percentage_local_original_guest'
percentage_local_original_host = 'percentage_local_original_host'
population_local_original_guest = 'population_local_original_guest'
population_local_original_host = 'population_local_original_host'

# table name
game_data = 'game_data'
prediction_data = 'prediction_data'


game_id = 'game_id'
play_time = 'play_time'
am_pm = 'AM_PM'
host_id = 'host_id'
guest_id = 'guest_id'
host_score = 'host_score'
guest_score = 'guest_score'
national_host_point_spread = 'host_point_spread'
win_if_meet_spread_point = 'win_if_meet_spread_point'
response_ratio_if_hit_spread_point = 'response_ratio_if_hit_spread_point'
national_total_point = 'national_total_point'
local_host_point_spread = 'local_host_point_spread'
local_total_point_threshold = 'local_total_point_threshold'
local_host_point_spread_response_ratio = 'local_host_point_spread_response_ratio'
local_total_point_threshold_response_ratio = 'local_total_point_threshold_response_ratio'
local_origin_guest_response_ratio = 'local_origin_guest_response_ratio'
local_origin_host_response_ratio = 'local_origin_host_response_ratio'
guest = 'guest'
host = 'host'

# prediction group
all_member = 'all_member'
more_than_sixty = 'more_than_sixty'
all_prefer = 'all_prefer'
top_100 = 'top_100'
prediction_group = {all_member: 0, more_than_sixty: 1, all_prefer: 2, top_100: 3}


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
                     '底特律活塞': 'DET',
                     '紐約尼克': 'NY',
                     '克里夫蘭騎士': 'CLE',
                     '印第安那溜馬': 'IND',
                     '多倫多暴龍': 'TOR',
                     '休士頓火箭': 'HOU',
                     '波士頓塞爾提克': 'BOS',
                     '費城76人': 'PHI',
                     '奧蘭多魔術': 'ORL',
                     '鳳凰城太陽': 'PHX',
                     '猶他爵士': 'UTA',
                     '布魯克林籃網': 'BKN',
                     '波特蘭拓荒者': 'POR',
                     '邁阿密熱火': 'MIA',
                     '芝加哥公牛': 'CHI',
                     '明尼蘇達灰狼': 'MIN'}

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
                                                      response_ratio_if_hit_spread_point,
                                                      national_total_point,
                                                      local_host_point_spread,
                                                      local_host_point_spread_response_ratio,
                                                      local_total_point_threshold,
                                                      local_total_point_threshold_response_ratio,
                                                      local_origin_guest_response_ratio,
                                                      local_origin_host_response_ratio))
