import os

import yaml

from config.constant import global_constant
from config.logger import get_logger


class Utility(object):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def load_environment_variable(self):
        self.logger.info('start load environment variables and overwrite config file')
        with open('config/configuration.yml') as config:
            config = yaml.load(config, Loader=yaml.FullLoader)

            config[global_constant.DB][global_constant.host] = os.environ.get('DB_HOST') if \
                os.environ.get('DB_HOST') else config[global_constant.DB][global_constant.host]

            config[global_constant.DB][global_constant.port] = int(os.environ.get('DB_PORT')) if \
                os.environ.get('DB_PORT') else config[global_constant.DB][global_constant.port]

            config[global_constant.DB][global_constant.user] = os.environ.get('DB_USERNAME') if \
                os.environ.get('DB_USERNAME') else config[global_constant.DB][global_constant.user]

            config[global_constant.DB][global_constant.password] = os.environ.get('DB_PASSWORD') if \
                os.environ.get('DB_PASSWORD') else config[global_constant.DB][global_constant.password]

        # overwrite config by environment variable
        with open('config/configuration.yml', 'w') as new_config:
            yaml.dump(config, new_config)

        self.logger.debug('finish update config file')
        return
