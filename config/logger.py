import logging
import datetime


def get_logger(player_id):

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s %(lineno)d %(name)s: %(levelname)s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S',
                        filename='log/{:%Y-%m-%d}.log'.format(datetime.datetime.now()))

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(filename)s %(lineno)d %(name)s: %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    logger = logging.getLogger(player_id)

    return logger
