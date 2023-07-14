# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import sys

LOG_PATH = "/var/log/sensor"

FORMATTER = logging.Formatter("[%(asctime)s]|%(levelname)s|%(process)d|%(thread)d|%(threadName)s"
                              "|%(filename)s|%(lineno)s|%(funcName)s|%(message)s")


def init(logger):
    logger.propagate = False
    logger.setLevel(logging.NOTSET)

    # 默认先输出到控制台
    t_handler = logging.StreamHandler(sys.stdout)
    t_handler.setFormatter(FORMATTER)
    logger.addHandler(t_handler)


def load(logger, path, level="info", count=0, w="H", i=1, suffix="%Y%m%d%H%M.log"):
    map_level = {"debug": logging.DEBUG, "info": logging.INFO, "warning": logging.WARNING, "error": logging.ERROR}
    i_level = map_level.get(level, logging.INFO)
    idx = path.rfind(os.sep)
    if idx > 2 and not os.path.exists(path[:idx]):
        os.makedirs(path[:idx], exist_ok=True)

    t_handler = logging.handlers.TimedRotatingFileHandler(filename=path, when=w, interval=i,
                                                          backupCount=count, encoding="utf-8")
    t_handler.suffix = suffix
    t_handler.setFormatter(FORMATTER)
    t_handler.setLevel(i_level)
    logger.addHandler(t_handler)


def get_logger():
    logger = logging.getLogger()
    if not logger.handlers:  # 判断logger是否被设置过了
        init(logger)
        load(logger, LOG_PATH + os.sep + 'sensor.log')
    return logger


def debug(msg):
    logger = get_logger()
    logger.debug(msg)


def info(msg):
    logger = get_logger()
    logger.info(msg)


def warning(msg):
    logger = get_logger()
    logger.warning(msg)


def error(msg):
    logger = get_logger()
    logger.error(msg)


g_logger = get_logger()  # getLogger与logging中采用相同的采用驼峰命名法
