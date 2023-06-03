import logging
import os
from typing import TypeVar

PathLike = TypeVar("PathLike", str, os.PathLike)


class CustomFormatter(logging.Formatter):
    """ Custom Formatter выполняет:
    Переопределяет значение поля 'funcName' значением 'func_name_override', если оно существует.
    """
    def format(self, record):
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override
        return super().format(record)


cur_dir: PathLike = os.path.dirname(__file__)

# Форматеры
formatter_funcinfo = CustomFormatter('%(asctime)s|%(levelname)s|%(funcName)s|%(message)s')

# Обработчики
handler_f_timeit = logging.FileHandler(filename=os.path.join(cur_dir, 'timeit.log'), encoding='utf-8')
handler_f_timeit.setLevel(logging.DEBUG)
handler_f_timeit.setFormatter(formatter_funcinfo)

handler_f_exception = logging.FileHandler(filename=os.path.join(cur_dir, 'exceptions.log'), encoding='utf-8')
handler_f_exception.setLevel(logging.DEBUG)
handler_f_exception.setFormatter(formatter_funcinfo)

handler_f_info = logging.FileHandler(filename=os.path.join(cur_dir, 'info.log'), encoding='utf-8')
handler_f_info.setLevel(logging.INFO)
handler_f_info.setFormatter(formatter_funcinfo)

handler_f_warning = logging.FileHandler(filename=os.path.join(cur_dir, 'warning.log'), encoding='utf-8')
handler_f_warning.setLevel(logging.WARNING)
handler_f_warning.setFormatter(formatter_funcinfo)

handler_console = logging.StreamHandler()
handler_console.setLevel(logging.INFO)


# Логгер для регистрации времени выполнения и записи в файл 'timeit.log'
logger_time = logging.getLogger('logger_time')
logger_time.setLevel(logging.DEBUG)
logger_time.addHandler(handler_f_timeit)
logger_time.addHandler(handler_console)

# Логгер для регистрации исключений и записи в файл 'exceptions.log'
logger_exception = logging.getLogger('logger_exception')
logger_exception.setLevel(logging.DEBUG)
logger_exception.addHandler(handler_f_exception)

# Логгер для регистрации общих событий и записи в файл 'info.log'
logger_info = logging.getLogger('logger_info')
logger_info.setLevel(logging.INFO)
# logger_info.addHandler(handler_console)
logger_info.addHandler(handler_f_info)

# Логгер для регистрации общих событий и записи в файл 'warning.log'
logger_warning = logging.getLogger('logger_warning')
logger_warning.setLevel(logging.WARNING)
logger_warning.addHandler(handler_console)
logger_warning.addHandler(handler_f_warning)
