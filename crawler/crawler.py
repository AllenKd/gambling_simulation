import datetime
import re
from collections import defaultdict

import pandas as pd
import pymysql
import requests
import yaml
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

from config import string_constant
from config.logger import get_logger
from crawler import constant


class Crawler(object):
    def __init__(self, start_date, total_day=None, end_date=None):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml') as config:
            self.config = yaml.load(config)
        self.data = None
        self.game_info = defaultdict(list)
        self.prediction_info_all_member = defaultdict(list)
        self.prediction_info_more_than_sixty = defaultdict(list)
        self.prediction_info_all_prefer = defaultdict(list)
        self.prediction_info_top_100 = defaultdict(list)

        self.prediction = {constant.all_member: self.prediction_info_all_member,
                           constant.more_than_sixty: self.prediction_info_more_than_sixty,
                           constant.all_prefer: self.prediction_info_all_prefer,
                           constant.top_100: self.prediction_info_top_100}

        self.start_date = datetime.datetime.strptime(start_date, '%Y%m%d')
        self.total_date = total_day
        self.end_date = self.start_date + datetime.timedelta(
            total_day) if total_day is not None else datetime.datetime.strptime(end_date, '%Y%m%d')

        # init db
        user = self.config[string_constant.DB][string_constant.user]
        password = self.config[string_constant.DB][string_constant.password]
        host = self.config[string_constant.DB][string_constant.host]
        self.engine = create_engine('mysql+pymysql://{}:{}@{}'.format(user, password, host))
        self.db = pymysql.connect(host=host, user=user, passwd=password,
                                  db=self.config[string_constant.DB][string_constant.schema], charset='utf8')

    def start_crawler(self):
        # crawl for each date
        for date in pd.date_range(start=self.start_date, end=self.end_date):
            # crawl for each prediction group
            for prediction_group in constant.prediction_group.keys():
                res = requests.get(self.get_url(date, constant.prediction_group[prediction_group]))
                soup = BeautifulSoup(res.text, 'html.parser')
                if prediction_group == constant.all_member:
                    # get game info for once
                    self.get_game_data(datetime.datetime.strftime(date, '%Y%m%d'), soup)
                    self.write_to_db(pd.DataFrame.from_dict(self.game_info))

                # get prediction info for each prediction group
                self.get_prediction_data(datetime.datetime.strftime(date, '%Y%m%d'), soup, prediction_group)

    def get_game_data(self, date, soup):
        self.logger.info('start crawl and parse data: {}'.format(date))
        custom_row = True
        for row_content in soup.find('tbody').findAll('tr', {'class': 'game-set'}):
            if custom_row:
                assert self.check_data_consistent()
                self.append_game_id(row_content, date)
                self.append_game_time(row_content)
                self.append_team_name(row_content)
                self.append_score(row_content)
                self.append_total_point_info(row_content)
            self.append_point_spread_info(row_content, custom_row)
            self.append_response_ratio_info(row_content, custom_row)
            custom_row = not custom_row
        self.logger.info('finished crawl and parse data: {}'.format(date))
        return

    def get_prediction_data(self, date, soup, group):
        guest_row = True
        for row_content in soup.find('tbody').findAll('tr', {'class': 'game-set'}):
            if guest_row:
                self.append_game_id(row_content, date, group)
            self.append_prediction_national_point_spread(row_content, guest_row, group)
            self.append_prediction_national_total_point(row_content, guest_row, group)
            self.append_prediction_local_point_spread(row_content, guest_row, group)
            self.append_prediction_local_total_point(row_content, guest_row, group)
            self.append_prediction_local_original(row_content, guest_row, group)
            guest_row = not guest_row

    def append_prediction_national_point_spread(self, row_content, guest_row, group):
        date = row_content.find('td', {'class': 'td-universal-bet01'}).find_next('td').text.strip()
        date = re.findall(r'\d+', date)
        percentage, population = date if len(date) == 2 else 0
        if guest_row:
            self.prediction[group][constant.percentage_national_point_spread_guest].append(percentage)
            self.prediction[group][constant.population_national_point_spread_guest].append(population)
        else:
            self.prediction[group][constant.percentage_national_point_spread_host].append(percentage)
            self.prediction[group][constant.population_national_point_spread_host].append(population)
        return

    def append_prediction_national_total_point(self, row_content, guest_row, group):
        date = row_content.find('td', {'class': 'td-universal-bet02'}).find_next('td').text.strip()
        date = re.findall(r'\d+', date)
        percentage, population = date if len(date) == 2 else 0
        if guest_row:
            self.prediction[group][constant.percentage_national_total_point_guest].append(percentage)
            self.prediction[group][constant.population_national_total_point_guest].append(population)
        else:
            self.prediction[group][constant.percentage_national_total_point_host].append(percentage)
            self.prediction[group][constant.population_national_total_point_host].append(population)
        return

    def append_prediction_local_point_spread(self, row_content, guest_row, group):
        date = row_content.find('td', {'class': 'td-bank-bet01'}).find_next('td').text.strip()
        date = re.findall(r'\d+', date)
        percentage, population = date if len(date) == 2 else 0
        if guest_row:
            self.prediction[group][constant.percentage_local_point_spread_guest].append(percentage)
            self.prediction[group][constant.population_local_point_spread_guest].append(population)
        else:
            self.prediction[group][constant.percentage_local_point_spread_host].append(percentage)
            self.prediction[group][constant.population_local_point_spread_host].append(population)
        return

    def append_prediction_local_total_point(self, row_content, guest_row, group):
        date = row_content.find('td', {'class': 'td-bank-bet02'}).find_next('td').text.strip()
        date = re.findall(r'\d+', date)
        percentage, population = date if len(date) == 2 else 0
        if guest_row:
            self.prediction[group][constant.percentage_local_total_point_guest].append(percentage)
            self.prediction[group][constant.population_local_total_point_guest].append(population)
        else:
            self.prediction[group][constant.percentage_local_total_point_host].append(percentage)
            self.prediction[group][constant.population_local_total_point_host].append(population)
        return

    def append_prediction_local_original(self, row_content, guest_row, group):
        date = row_content.find('td', {'class': 'td-bank-bet03'}).find_next('td').text.strip()
        date = re.findall(r'\d+', date)
        percentage, population = date if len(date) == 2 else 0
        if guest_row:
            self.prediction[group][constant.percentage_local_original_guest].append(percentage)
            self.prediction[group][constant.population_local_original_guest].append(population)
        else:
            self.prediction[group][constant.percentage_local_original_host].append(percentage)
            self.prediction[group][constant.population_local_original_host].append(population)
        return

    def append_game_id(self, row_content, date, group=None):
        self.logger.info(
            'current column size of {}: {}'.format(constant.game_id, len(self.game_info[constant.game_id])))
        game_id = date + row_content.find('td', 'td-gameinfo').find('h3').text
        self.logger.info('append game id: {}'.format(game_id))
        if group:
            self.prediction[group][constant.game_id].append(game_id)
        else:
            self.game_info[constant.game_id].append(game_id)
        return

    def append_game_time(self, row_content):
        self.logger.info(
            'current column size of {}: {}'.format(constant.play_time, len(self.game_info[constant.play_time])))
        game_time = row_content.find('td', 'td-gameinfo').find('h4').text
        self.logger.info('append play time: {}'.format(game_time))
        self.game_info[constant.play_time].append(game_time)
        return

    def append_score(self, row_content):
        self.logger.info(
            'current column size of {}: {}'.format(constant.guest_score, len(self.game_info[constant.guest_score])))
        self.logger.info(
            'current column size of {}: {}'.format(constant.host_score, len(self.game_info[constant.host_score])))
        guest = int(row_content.find('td', {'class': 'td-teaminfo'}).find_all('li')[0].text.strip())
        host = int(row_content.find('td', {'class': 'td-teaminfo'}).find_all('li')[-1].text.strip())
        self.logger.debug('append guest: {}, host: {}'.format(guest, host))
        self.game_info[constant.guest_score].append(guest)
        self.game_info[constant.host_score].append(host)
        return

    def append_team_name(self, row_content):
        self.logger.info(
            'current column size of {}: {}'.format(constant.guest_id, len(self.game_info[constant.guest])))
        self.logger.info(
            'current column size of {}: {}'.format(constant.host_id, len(self.game_info[constant.host])))

        guest = row_content.find('td', {'class': 'td-teaminfo'}).find_all('tr')[0].find('a').text.strip()
        host = row_content.find('td', {'class': 'td-teaminfo'}).find_all('tr')[-1].find('a').text.strip()

        self.logger.debug('append guest: {}, host: {}'.format(guest, host))
        self.game_info[constant.guest].append(constant.team_name_mapping[guest])
        self.game_info[constant.host].append(constant.team_name_mapping[host])
        return

    def append_point_spread_info(self, row_content, custom_row):
        spread_info = row_content.find('td', {'class': 'td-universal-bet01'}).text.strip()
        if len(spread_info) != 1:
            # get national point spread info
            self.logger.info('the row contains national spread point info')
            national_spread_from = constant.chinese_mapping[spread_info[0]]
            national_spread_point, hit_percentage = re.findall(r'\d+', spread_info)
            hit_result = constant.chinese_mapping[re.findall(r'[輸贏]', spread_info)[0]]
            hit_percentage = int(hit_percentage) + 100 if hit_result else int(hit_percentage)
            national_spread_point = -int(national_spread_point) if national_spread_from == constant.guest else int(
                national_spread_point)
            self.game_info[constant.national_host_point_spread].append(national_spread_point)
            self.game_info[constant.win_if_meet_spread_point].append(hit_result)
            self.game_info[constant.response_if_meet_spread_point].append(hit_percentage)

        if custom_row:
            # get local point spread info and response ratio
            local_host_spread_point = row_content.find('td', {'class': 'td-bank-bet01'}).text.strip()
            # filter out float
            data = re.findall(r'[+-]?\d+\.\d+', local_host_spread_point)
            local_host_spread_point, spread_point_response_ratio = data if len(data) == 2 else 0
            self.game_info[constant.local_host_point_spread].append(float(local_host_spread_point))
            self.game_info[constant.local_host_point_spread_response_ratio].append(float(spread_point_response_ratio))

            # get local total point info and response ratio
            local_total_point = row_content.find('td', {'class': 'td-bank-bet02'}).text.strip()
            # filter out float
            data = re.findall(r'\d+\.\d+', local_total_point)
            local_total_point, total_point_response = data if len(data) == 2 else 0
            self.game_info[constant.local_total_point_threshold].append(float(local_total_point))
            self.game_info[constant.local_total_point_threshold_response_ratio].append(float(total_point_response))

        return

    def append_total_point_info(self, row_content):
        # get national total point info
        national_total_point = row_content.find('td', {'class': 'td-universal-bet02'}).text.strip()
        threshold = re.findall(r'\d+\.\d+', national_total_point)
        national_total_point = threshold[0] if threshold else 0
        self.game_info[constant.national_total_point].append(float(national_total_point))
        pass

    def append_response_ratio_info(self, row_content, guest_row):
        self.logger.info('append response ratio info')
        if guest_row:
            # get guest response ratio of no point spread at local
            local_origin_guest_response_ratio = row_content.find('td', {'class': 'td-bank-bet03'}).text.strip()
            ratio = re.findall(r'\d+\.\d+', local_origin_guest_response_ratio)
            local_origin_guest_response_ratio = ratio[0] if ratio else 0
            self.game_info[constant.local_origin_guest_response_ratio].append(float(local_origin_guest_response_ratio))
        else:
            # get host response ratio of no point spread at local
            local_origin_host_response_ratio = row_content.find('td', {'class': 'td-bank-bet03'}).text.strip()
            ratio = re.findall(r'\d+\.\d+', local_origin_host_response_ratio)
            local_origin_host_response_ratio = ratio[0] if ratio else 0
            self.game_info[constant.local_origin_host_response_ratio].append(float(local_origin_host_response_ratio))

    def write_to_db(self, game_data):
        self.logger.info('start write game data to db')
        game_data.to_sql(con=self.engine,
                         name='game_info',
                         if_exists='append',
                         schema=self.config[string_constant.DB][string_constant.schema])
        return

    def check_data_consistent(self):
        length_list = [len(i) for i in self.game_info.values()]
        return length_list.count(length_list[0]) == len(length_list) if length_list else True

    def get_url(self, date, member_type=1):
        return self.config['crawler']['urlPattern'].format(date, member_type)
