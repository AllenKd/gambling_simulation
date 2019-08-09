import datetime
import time

import click
import schedule
import yaml
from dateutil.relativedelta import relativedelta

from analyzer.crawled_result_analyzer import CrawledResultAnalyzer
from config.constant import global_constant
from config.constant import player as player_constant
from crawler.crawler import Crawler
from crawler.data_updater import DataUpdater
from database.constructor import DbConstructor
from game_predictor.data_backup_scheduler import DataBackupScheduler
from simulator.simulator import Simulator
from utility.utility import Utility


@click.group(chain=True)
def cli():
    pass


@click.command('simulate_gambling', help='Simulate gambling.')
@click.option('--num_of_player', '-p',
              type=int,
              default=10,
              help='Number of player of each put strategy in the gambling', show_default=True)
@click.option('--bet_strategy', '-bs',
              type=click.Choice([player_constant.random, player_constant.follow_last, player_constant.keep_false,
                                 player_constant.keep_true]),
              default=player_constant.random,
              help='Bet strategy of each player.', show_default=True)
@click.option('--game_times', '-gt',
              type=int,
              default=100,
              help='Gambling times.', show_default=True)
@click.option('--init_money', '-im',
              type=int,
              default=10000,
              help='Initial money of each player.', show_default=True)
def task_simulator(game_times, num_of_player, bet_strategy, init_money):
    strategy_list = [player_constant.kelly, player_constant.linear_response, player_constant.fibonacci_base,
                     player_constant.foo_double] * num_of_player
    simulator = Simulator(play_times=game_times, number_of_player=len(strategy_list), player_init_money=init_money,
                          to_db=True, player_put_strategy=strategy_list, player_bet_strategy=bet_strategy)
    simulator.start_simulation()


@click.command('create_db', help='Create DB.')
@click.option('--force', '-f',
              is_flag=True,
              default=False,
              help='Drop schema before create.', show_default=True)
@click.option('--create_schema', '-cs',
              is_flag=True,
              default=False,
              help='Create schema.', show_default=True)
@click.option('--create_table', '-ct',
              is_flag=True,
              default=True,
              help='Create table.', show_default=True)
def task_create_db(force, create_schema, create_table):
    b = DbConstructor()
    if create_schema:
        b.create_schema(force=force)
    if create_table:
        b.create_tables()


@click.command('crawl_data', help='Start crawler to get sports gambling data.')
@click.option('--start_date', '-sd',
              type=str,
              required=False,
              default=datetime.datetime.strftime(datetime.datetime.now() - relativedelta(days=7), '%Y%m%d'),
              show_default=True,
              help='Start date of sports gambling, the format must follow the pattern: YYYYmmDD, ex: 20190130.')
@click.option('--end_date', '-ed',
              type=str,
              required=False,
              default=datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'),
              show_default=True,
              help='End date of sports gambling, the format must follow the pattern: YYYYmmDD, ex: 20190130.')
@click.option('--game_type', '-gt',
              type=click.Choice(global_constant.game_type_map.keys()),
              default=global_constant.NBA,
              help='Target game type.', show_default=True)
def task_crawler(start_date, end_date, game_type):
    Crawler(start_date=start_date, end_date=end_date, game_type=game_type).start_crawler()


@click.command('update_db', help='Update game data based on game_season.yml')
@click.option('--keep_update', '-k',
              is_flag=True,
              default=False,
              help='Keeping update.', show_default=True)
def task_update_db(keep_update):
    if keep_update:
        with open('config/configuration.yml') as config:
            config = yaml.load(config, Loader=yaml.FullLoader)
        Utility().load_environment_variable()
        schedule.every(config['data_updater']['update_period']).hours.do(DataUpdater().update_db)
        schedule.every(config['data_updater']['backup_period']).days.do(DataBackupScheduler.backup, True)

        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        DataUpdater().update_db()


@click.command('analyze', help='Make judgement about crawled data.')
@click.option('--to_db', '-td',
              is_flag=True,
              default=False,
              help='Write analyzed result to db.', show_default=True)
def task_analyzer(to_db):
    CrawledResultAnalyzer(to_db=to_db).start_analyze()


@click.command('backup', help='Backup database.')
def task_backup():
    DataBackupScheduler().backup()


@click.command('restore', help='Restore data from backuped sql files.')
@click.option('--sql_file', '-f',
              type=str,
              required=False,
              default=None,
              show_default=True,
              help='Specific sql file. ex: ./backup_file.sql')
def task_data_restore(sql_file):
    if sql_file:
        DataBackupScheduler().data_restore_worker(sql_file)
    else:
        DataBackupScheduler().data_restore()


@click.command('reset_id', help='Reset table auto-increment key.')
def task_reset_id():
    DataBackupScheduler().reset_id()


if __name__ == '__main__':
    cli.add_command(task_simulator)
    cli.add_command(task_create_db)
    cli.add_command(task_crawler)
    cli.add_command(task_analyzer)
    cli.add_command(task_backup)
    cli.add_command(task_data_restore)
    cli.add_command(task_reset_id)
    cli.add_command(task_update_db)
    cli()
