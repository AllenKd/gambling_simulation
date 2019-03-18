import logging


def get_logger(player_id):

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s %(lineno)d: %(levelname)s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S',
                        filename='logfile')

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(filename)s %(lineno)d: %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    logger = logging.getLogger(player_id)

    return logger
