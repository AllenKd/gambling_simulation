import click

from banker.banker import Banker
from gambler.gambler import Gambler
from game_predictor.data_backup_scheduler import DataBackupScheduler
from strategy_provider.foo_double import FooDouble
from mongodb.init_db import init_mongo

# from simulator.simulator import Simulator


@click.group(chain=True)
def cli():
    pass


@click.command("backup", help="Backup database.")
def task_backup():
    DataBackupScheduler().backup()


@click.command("restore", help="Restore data from backuped sql files.")
@click.option(
    "--sql_file",
    "-f",
    type=str,
    required=False,
    default=None,
    show_default=True,
    help="Specific sql file. ex: ./backup_file.sql",
)
def task_data_restore(sql_file):
    if sql_file:
        DataBackupScheduler().data_restore_worker(sql_file)
    else:
        DataBackupScheduler().data_restore()


@click.command("reset_id", help="Reset table auto-increment key.")
def task_reset_id():
    DataBackupScheduler().reset_id()


@click.command("test")
def test_banker():
    # Banker().get_gamble_info('20180724', gamble_id=215)
    Banker().get_gamble_info("20180724", game_type="MLB")


@click.command("test_gambler")
def test_gambler():
    init_mongo()
    Gambler(
        gambler_id=1, principle=5000, strategy_provider=FooDouble("NBA", "foo double")
    ).battle(start_date="20180925")


if __name__ == "__main__":
    cli.add_command(task_backup)
    cli.add_command(task_data_restore)
    cli.add_command(task_reset_id)
    cli.add_command(test_banker)
    cli.add_command(test_gambler)
    cli()
