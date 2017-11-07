# coding=utf-8
"""
provide logger from logging
"""
import logging
from logging.handlers import TimedRotatingFileHandler
from .config import LOG_PATH


def get_root_logger():
    logger = logging.getLogger()
    formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s')
    fh = TimedRotatingFileHandler(LOG_PATH, when='midnight', encoding='utf-8')
    fh.suffix = '%Y_%m_%d.log'
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(fh)
    return logger
