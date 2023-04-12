import functools
import time
import rapidjson

from mainapp.processing.handlers.exception_case import exception_replies


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
        def wrapper(event):
            try:
                return func(event)
            except Exception as err:
                event_dict = rapidjson.loads(event.body)
                command: str = event_dict['request']['command']
                logger.exception(f'exception:{err}|command:{command!r}', extra={'func_name_override': func.__name__})
                return exception_replies(event_dict, err)
        return wrapper
    return decorator