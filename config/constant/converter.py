# from config.constant import database as db_constant
# from config.constant import crawler
#
joined_columns = [
    'game_data.id',
    'game_data.game_date',
    'game_data.gamble_id',
    'game_data.game_type',
    'game_data.play_time',
    'game_data.AM_PM',
    'game_data.guest',
    'game_data.host',
    'game_data.guest_score',
    'game_data.host_score',
    'game_data.national_total_point_threshold',
    'game_data.national_host_point_spread',
    'game_data.win_if_meet_spread_point',
    'game_data.response_ratio_if_hit_spread_point',
    'game_data.local_host_point_spread',
    'game_data.local_host_point_spread_response_ratio',
    'game_data.local_total_point_threshold',
    'game_data.local_total_point_threshold_response_ratio',
    'game_data.local_origin_guest_response_ratio',
    'game_data.local_origin_host_response_ratio',
    'game_judgement.host_win_original',
    'game_judgement.host_win_point_spread_national',
    'game_judgement.host_win_point_spread_local',
    'game_judgement.over_total_point_national',
    'game_judgement.over_total_point_local',
    'prediction_data_all_member.percentage_national_point_spread_guest AS percentage_national_point_spread_guest-all_member',
    'prediction_data_all_member.population_national_point_spread_guest AS population_national_point_spread_guest-all_member',
    'prediction_data_all_member.percentage_national_total_point_over AS percentage_national_total_point_over-all_member',
    'prediction_data_all_member.population_national_total_point_over AS population_national_total_point_over-all_member',
    'prediction_data_all_member.percentage_local_point_spread_guest AS percentage_local_point_spread_guest-all_member',
    'prediction_data_all_member.population_local_point_spread_guest AS population_local_point_spread_guest-all_member',
    'prediction_data_all_member.percentage_local_total_point_over AS percentage_local_total_point_over-all_member',
    'prediction_data_all_member.population_local_total_point_over AS population_local_total_point_over-all_member',
    'prediction_data_all_member.percentage_local_original_guest AS percentage_local_original_guest-all_member',
    'prediction_data_all_member.population_local_original_guest AS population_local_original_guest-all_member',
    'prediction_data_all_member.percentage_national_point_spread_host AS percentage_national_point_spread_host-all_member',
    'prediction_data_all_member.population_national_point_spread_host AS population_national_point_spread_host-all_member',
    'prediction_data_all_member.percentage_national_total_point_under AS percentage_national_total_point_under-all_member',
    'prediction_data_all_member.population_national_total_point_under AS population_national_total_point_under-all_member',
    'prediction_data_all_member.percentage_local_point_spread_host AS percentage_local_point_spread_host-all_member',
    'prediction_data_all_member.population_local_point_spread_host AS population_local_point_spread_host-all_member',
    'prediction_data_all_member.percentage_local_total_point_under AS percentage_local_total_point_under-all_member',
    'prediction_data_all_member.population_local_total_point_under AS population_local_total_point_under-all_member',
    'prediction_data_all_member.percentage_local_original_host AS percentage_local_original_host-all_member',
    'prediction_data_all_member.population_local_original_host AS population_local_original_host-all_member',
    'prediction_data_all_prefer.percentage_national_point_spread_guest AS percentage_national_point_spread_guest-all_prefer',
    'prediction_data_all_prefer.population_national_point_spread_guest AS population_national_point_spread_guest-all_prefer',
    'prediction_data_all_prefer.percentage_national_total_point_over AS percentage_national_total_point_over-all_prefer',
    'prediction_data_all_prefer.population_national_total_point_over AS population_national_total_point_over-all_prefer',
    'prediction_data_all_prefer.percentage_local_point_spread_guest AS percentage_local_point_spread_guest-all_prefer',
    'prediction_data_all_prefer.population_local_point_spread_guest AS population_local_point_spread_guest-all_prefer',
    'prediction_data_all_prefer.percentage_local_total_point_over AS percentage_local_total_point_over-all_prefer',
    'prediction_data_all_prefer.population_local_total_point_over AS population_local_total_point_over-all_prefer',
    'prediction_data_all_prefer.percentage_local_original_guest AS percentage_local_original_guest-all_prefer',
    'prediction_data_all_prefer.population_local_original_guest AS population_local_original_guest-all_prefer',
    'prediction_data_all_prefer.percentage_national_point_spread_host AS percentage_national_point_spread_host-all_prefer',
    'prediction_data_all_prefer.population_national_point_spread_host AS population_national_point_spread_host-all_prefer',
    'prediction_data_all_prefer.percentage_national_total_point_under AS percentage_national_total_point_under-all_prefer',
    'prediction_data_all_prefer.population_national_total_point_under AS population_national_total_point_under-all_prefer',
    'prediction_data_all_prefer.percentage_local_point_spread_host AS percentage_local_point_spread_host-all_prefer',
    'prediction_data_all_prefer.population_local_point_spread_host AS population_local_point_spread_host-all_prefer',
    'prediction_data_all_prefer.percentage_local_total_point_under AS percentage_local_total_point_under-all_prefer',
    'prediction_data_all_prefer.population_local_total_point_under AS population_local_total_point_under-all_prefer',
    'prediction_data_all_prefer.percentage_local_original_host AS percentage_local_original_host-all_prefer',
    'prediction_data_all_prefer.population_local_original_host AS population_local_original_host-all_prefer',
    'prediction_data_more_than_sixty.percentage_national_point_spread_guest AS percentage_national_point_spread_guest-more_than_sixty',
    'prediction_data_more_than_sixty.population_national_point_spread_guest AS population_national_point_spread_guest-more_than_sixty',
    'prediction_data_more_than_sixty.percentage_national_total_point_over AS percentage_national_total_point_over-more_than_sixty',
    'prediction_data_more_than_sixty.population_national_total_point_over AS population_national_total_point_over-more_than_sixty',
    'prediction_data_more_than_sixty.percentage_local_point_spread_guest AS percentage_local_point_spread_guest-more_than_sixty',
    'prediction_data_more_than_sixty.population_local_point_spread_guest AS population_local_point_spread_guest-more_than_sixty',
    'prediction_data_more_than_sixty.percentage_local_total_point_over AS percentage_local_total_point_over-more_than_sixty',
    'prediction_data_more_than_sixty.population_local_total_point_over AS population_local_total_point_over-more_than_sixty',
    'prediction_data_more_than_sixty.percentage_local_original_guest AS percentage_local_original_guest-more_than_sixty',
    'prediction_data_more_than_sixty.population_local_original_guest AS population_local_original_guest-more_than_sixty',
    'prediction_data_more_than_sixty.percentage_national_point_spread_host AS percentage_national_point_spread_host-more_than_sixty',
    'prediction_data_more_than_sixty.population_national_point_spread_host AS population_national_point_spread_host-more_than_sixty',
    'prediction_data_more_than_sixty.percentage_national_total_point_under AS percentage_national_total_point_under-more_than_sixty',
    'prediction_data_more_than_sixty.population_national_total_point_under AS population_national_total_point_under-more_than_sixty',
    'prediction_data_more_than_sixty.percentage_local_point_spread_host AS percentage_local_point_spread_host-more_than_sixty',
    'prediction_data_more_than_sixty.population_local_point_spread_host AS population_local_point_spread_host-more_than_sixty',
    'prediction_data_more_than_sixty.percentage_local_total_point_under AS percentage_local_total_point_under-more_than_sixty',
    'prediction_data_more_than_sixty.population_local_total_point_under AS population_local_total_point_under-more_than_sixty',
    'prediction_data_more_than_sixty.percentage_local_original_host AS percentage_local_original_host-more_than_sixty',
    'prediction_data_more_than_sixty.population_local_original_host AS population_local_original_host-more_than_sixty',
    'prediction_data_top_100.percentage_national_point_spread_guest AS percentage_national_point_spread_guest-top_100',
    'prediction_data_top_100.population_national_point_spread_guest AS population_national_point_spread_guest-top_100',
    'prediction_data_top_100.percentage_national_total_point_over AS percentage_national_total_point_over-top_100',
    'prediction_data_top_100.population_national_total_point_over AS population_national_total_point_over-top_100',
    'prediction_data_top_100.percentage_local_point_spread_guest AS percentage_local_point_spread_guest-top_100',
    'prediction_data_top_100.population_local_point_spread_guest AS population_local_point_spread_guest-top_100',
    'prediction_data_top_100.percentage_local_total_point_over AS percentage_local_total_point_over-top_100',
    'prediction_data_top_100.population_local_total_point_over AS population_local_total_point_over-top_100',
    'prediction_data_top_100.percentage_local_original_guest AS percentage_local_original_guest-top_100',
    'prediction_data_top_100.population_local_original_guest AS population_local_original_guest-top_100',
    'prediction_data_top_100.percentage_national_point_spread_host AS percentage_national_point_spread_host-top_100',
    'prediction_data_top_100.population_national_point_spread_host AS population_national_point_spread_host-top_100',
    'prediction_data_top_100.percentage_national_total_point_under AS percentage_national_total_point_under-top_100',
    'prediction_data_top_100.population_national_total_point_under AS population_national_total_point_under-top_100',
    'prediction_data_top_100.percentage_local_point_spread_host AS percentage_local_point_spread_host-top_100',
    'prediction_data_top_100.population_local_point_spread_host AS population_local_point_spread_host-top_100',
    'prediction_data_top_100.percentage_local_total_point_under AS percentage_local_total_point_under-top_100',
    'prediction_data_top_100.population_local_total_point_under AS population_local_total_point_under-top_100',
    'prediction_data_top_100.percentage_local_original_host AS percentage_local_original_host-top_100',
    'prediction_data_top_100.population_local_original_host AS population_local_original_host-top_100']
