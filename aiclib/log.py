import logging


FMT = ("%(asctime)s %(process)d %(levelname)s %(name)s [-] %(message)s func"
       " %(pathname)s:%(lineno)d")

logging.basicConfig(format=FMT, level=logging.INFO)


def get_logger(name):
    #TODO(mdietz): we probably want to allow passing of a full logging config
    logger = logging.getLogger(name)
    return logger
