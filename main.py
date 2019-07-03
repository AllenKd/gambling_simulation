import click

from analyzer.crawled_result_analyzer import CrawledResultAnalyzer
from config.constant import player as player_constant
from database.constructor import DbConstructor
from simulator.simulator import Simulator


@click.group()
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
def task_create_db(force):
    b = DbConstructor()
    b.create_schema(force=force)
    b.create_tables()


@click.command('crawl_data', help='Start crawler to get sports gambling data.')
@click.option('--start_date', '-sd',
              type=str,
              required=True,
              help='Start date of sports gambling, the format must follow the pattern: YYYYmmDD, ex: 20190130.')
def task_crawler(start_date):
    import datetime
    from crawler.crawler import Crawler
    a = Crawler(start_date=start_date, end_date=datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'))
    a.start_crawler()


@click.command('analyze', help='Make judgement about crawled data.')
@click.option('--to_db', '-td',
              is_flag=True,
              default=False,
              help='Write analyzed result to db.', show_default=True)
def task_analyzer(to_db):
    a = CrawledResultAnalyzer(to_db=to_db)
    a.start_analyzer()


cli.add_command(task_simulator)
cli.add_command(task_create_db)
cli.add_command(task_crawler)
cli.add_command(task_analyzer)

if __name__ == '__main__':
    cli()
    # task_create_db()
    # task_crawler()
    # task_analyzer()
    # task_simulator(1)
