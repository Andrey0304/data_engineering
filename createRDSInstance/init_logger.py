from functools import wraps
import logging
import sys


def log(level='WARNING'):
    def log_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as ex:
                logger = logging.getLogger(f'{function.__name__}')
                loggers = {
                           'WARNING': logger.warning,
                           'ERROR': logger.error,
                           'CRITICAL': logger.critical
                           }
                loggers[level](ex)
            if level == 'CRITICAL':
                sys.exit()
        return wrapper
    return log_decorator