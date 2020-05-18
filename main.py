import datetime

import click
from dateutil.relativedelta import relativedelta
from game_predictor.traninig_data.generator import TrainingDataGenerator
from mongodb.init_db import init_mongo

from simulator.simulator import Simulator


@click.group(chain=True)
def cli():
    pass


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
def run_simulator(start_date, principle):
    Simulator(start_date=start_date, principle=principle).start_simulation()


@click.command("init_mongo")
def init_mg():
    init_mongo()


@click.command("init_training_data")
def init_training_data():
    TrainingDataGenerator().gen_confidence_data()


from game_predictor.models.train.confidence_to_prob import confidence_to_prob
@click.command("test")
def testing():
    confidence_to_prob('all')
    confidence_to_prob('nba', game_filter={'game_type': "NBA"})
    confidence_to_prob('mlb', game_filter={'game_type': "MLB"})
    confidence_to_prob('npb', game_filter={'game_type': "NPB"})


if __name__ == "__main__":
    cli.add_command(run_simulator)
    cli.add_command(init_training_data)
    cli.add_command(init_mg)
    cli.add_command(testing)
    cli()
