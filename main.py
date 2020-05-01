import datetime

import click
from dateutil.relativedelta import relativedelta

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


if __name__ == "__main__":
    cli.add_command(run_simulator)
    cli()
