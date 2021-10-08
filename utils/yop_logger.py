# -*- coding: utf-8 -*-

# @title : 封装Logging
# @Author : dreambt
# @Date : 20/11/30
# @Desc :

import logging


def get_logger(logger_name=__name__):
    """
    Get a logger.

    Args:
        logger_name: write your description
        __name__: write your description
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)

    if len(logger.handlers) == 0:
        hdl = logging.StreamHandler()
        # hdl = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        hdl.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(thread)d - %(filename)s[:%(lineno)d] - %(message)s'))
        hdl.setLevel(logging.DEBUG)
        logger.addHandler(hdl)

    return logger
