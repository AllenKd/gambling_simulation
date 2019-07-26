from config.constant import crawler
from config.constant import database as db_constant

table_list = [db_constant.game_data,
              db_constant.game_judgement,
              '{}_{}'.format(db_constant.prediction_data, crawler.all_member),
              '{}_{}'.format(db_constant.prediction_data, crawler.all_prefer),
              '{}_{}'.format(db_constant.prediction_data, crawler.more_than_sixty),
              '{}_{}'.format(db_constant.prediction_data, crawler.top_100),
              '{}_{}'.format(db_constant.prediction_judgement, crawler.all_member),
              '{}_{}'.format(db_constant.prediction_judgement, crawler.all_prefer),
              '{}_{}'.format(db_constant.prediction_judgement, crawler.more_than_sixty),
              '{}_{}'.format(db_constant.prediction_judgement, crawler.top_100)]

start = 'start'
end = 'end'
