import datetime

import click
from dateutil.relativedelta import relativedelta

from banker.banker import Banker
from gambler.gambler import Gambler
from mongodb.init_db import init_mongo
from simulator.simulator import Simulator
from strategy_provider.bet_strategy.constant import Constant
from strategy_provider.put_strategy.linear_response import LinearResponse


# from simulator.simulator import Simulator


@click.group(chain=True)
def cli():
    pass


# TODO: move to uni test
@click.command("test")
def test_banker():
    # Banker().get_gamble_info('20180724', gamble_id=215)
    Banker().get_gamble_info("20180724", game_type="MLB")


@click.command("run_simulator")
@click.option(
    "--start_date",
    "-sd",
    type=str,
    required=False,
    default=datetime.datetime.strftime(
        datetime.datetime.now() - relativedelta(days=7), "%Y%m%d"
    ),
    show_default=True,
    help="Start date of gambling, the format must follow the pattern: YYYYmmDD, ex: 20190130.",
)
@click.option(
    "--principle",
    "-p",
    type=int,
    required=False,
    default=100,
    show_default=True,
    help="Default principle unit of each gambler.",
)
def run_simulator():
    Simulator().start_simulation()


@click.command("test_gambler")
def test_gambler():
    init_mongo()
    # Gambler(
    #     gambler_id=1, principle=5000, strategy_provider=FooDouble("NBA", "foo double", PutStrategyFooDouble('foo double'))
    # ).battle(start_date="20180929")
    Gambler(
        gambler_id=1, principle=100, strategy_provider=Constant(LinearResponse()),
    ).battle(start_date="20180929")


if __name__ == "__main__":
    cli.add_command(test_banker)
    cli.add_command(test_gambler)
    cli.add_command(run_simulator)
    cli()
