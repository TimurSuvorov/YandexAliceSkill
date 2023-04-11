import functools
import os
import time
from inspect import getframeinfo, stack

from mainapp.logging.custom_loggers import logger_exception


# Декоратор для логирования времени выполнения функции
def timeit_logger(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            st_time = time.perf_counter()
            func_res = func(*args, **kwargs)
            res_time = time.perf_counter() - st_time
            logger.info(f"time: {res_time}", extra={'func_name_override': func.__name__})
            return func_res
        return wrapper
    return decorator


# Декоратор для логирования исключений в функции
def exception_logger(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print('Пошло: ', func.__name__)
                return func(*args, **kwargs)
            except Exception as err:
                logger.exception(f'exception:{err}|Args:{args!r}', extra={'func_name_override': func.__name__})
                print('Не прошло и записалось: ', func.__name__)
                return f'Error: {err}'
        return wrapper
    return decorator
