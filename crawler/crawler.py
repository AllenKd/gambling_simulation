import requests
import yaml
import re
from crawler import constant
from bs4 import BeautifulSoup
from config.logger import get_logger
from collections import defaultdict


class Crawler(object):
    def __init__(self, start_date, total_date=None, end_date=None):
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml') as config:
            self.config = yaml.load(config)
        self.data = None
        self.game_info = defaultdict(list)
        self.prediction_info_all_member = defaultdict(list)
        self.prediction_info_more_than_sixty = defaultdict(list)
        self.prediction_info_all_prefer = defaultdict(list)
        self.prediction_info_top_100 = defaultdict(list)

    def get_game_data(self, date):
        for member_type in self.config['crawler']['memberType'].values():
            res = requests.get(self.get_url(date, member_type))
            soup = BeautifulSoup(res.text, 'html.parser')

            custom_row = True
            for row_content in soup.find('tbody').findAll('tr', {'class': 'game-set'}):
                if custom_row:
                    self.append_game_id(row_content)
                    self.append_game_time(row_content)
                    self.append_team_name(row_content)
                    self.append_score(row_content)
                self.append_point_spread_info(row_content, custom_row)

                custom_row = not custom_row
                assert self.check_data_consistent()
            return

    def append_game_id(self, row_content):
        self.logger.info(
            'current column size of {}: {}'.format(constant.game_id, len(self.game_info[constant.game_id])))
        game_id = row_content.find('td', 'td-gameinfo').find('h3').text
        self.logger.info('append game id: {}'.format(game_id))
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
            'current column size of {}: {}'.format(constant.guest_id, len(self.game_info[constant.guest_id])))
        self.logger.info(
            'current column size of {}: {}'.format(constant.host_id, len(self.game_info[constant.host_id])))

        guest = row_content.find('td', {'class': 'td-teaminfo'}).find_all('tr')[0].find('a').text.strip()
        host = row_content.find('td', {'class': 'td-teaminfo'}).find_all('tr')[-1].find('a').text.strip()

        self.logger.debug('append guest: {}, host: {}'.format(guest, host))
        self.game_info[constant.guest_id].append(guest)
        self.game_info[constant.host_id].append(host)
        return

    def get_prediction_data(self, row_text_list):
        pass

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
            # get national total point info
            national_total_point = row_content.find('td', {'class': 'td-universal-bet02'}).text.strip()
            national_total_point = re.findall(r'\d+\.\d+', national_total_point)[0]  # filter our first float
            self.game_info[constant.national_total_point].append(float(national_total_point))

            # get local point spread info
            local_host_spread_point = row_content.find('td', {'class': 'td-bank-bet01'}).text.strip()
            # filter out float
            local_host_spread_point, spread_point_response_ratio = re.findall(r'[+-]?\d+\.\d+', local_host_spread_point)
            self.game_info[constant.local_host_point_spread].append(float(local_host_spread_point))
            self.game_info[constant.local_host_point_spread_response_ratio].append(float(spread_point_response_ratio))

            # get local total point info
            local_total_point = row_content.find('td', {'class': 'td-bank-bet02'}).text.strip()
            # filter out float
            local_total_point, total_point_response = re.findall(r'\d+\.\d+', local_total_point)
            self.game_info[constant.local_total_point_threshold].append(float(local_total_point))
            self.game_info[constant.local_total_point_threshold_response_ratio].append(float(total_point_response))

            # get guest response ratio of no point spread at local
            local_origin_guest_response_ratio = row_content.find('td', {'class': 'td-bank-bet03'}).text.strip()
            local_origin_guest_response_ratio = re.findall(r'\d+\.\d+', local_origin_guest_response_ratio)[0]
            self.game_info[constant.local_origin_guest_response_ratio].append(float(local_origin_guest_response_ratio))
        else:
            # get host response ratio of no point spread at local
            local_origin_host_response_ratio = row_content.find('td', {'class': 'td-bank-bet03'}).text.strip()
            local_origin_host_response_ratio = re.findall(r'\d+\.\d+', local_origin_host_response_ratio)[0]
            self.game_info[constant.local_origin_host_response_ratio].append(float(local_origin_host_response_ratio))

        return

    def check_data_consistent(self):
        length_list = [len(i) for i in self.game_info.values()]
        return length_list.count(length_list[0]) == len(length_list)

    def get_url(self, date, member_type=1):
        return self.config['crawler']['urlPattern'].format(date, member_type)


if __name__ == '__main__':
    # url = 'https://www.playsport.cc/predictgame.php?action=scale&allianceid=3&gametime=20190402&sid=0'
    # get_game_result(url)
    a = Crawler('20190401')
    a.get_game_data('20190401')
    b = a.get_url('20190401', 0)
    print('fwefw')
