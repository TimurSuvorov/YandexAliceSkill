import datetime
import json
import rapidjson
import os
import time
import logging
from pprint import pprint

cur_dir = os.path.dirname(os.path.abspath(__file__))
USERFOLDER = os.path.join(cur_dir, 'userfiles')


def check_old_user(user_id: str, session_id: str):
    """
    Функция открывает профайл пользователя и по количеству ключей проверяет новый пользователь или нет.
    Если ключей больше 4 (исходный сет значений[3] + запись текущей сессии[1])
    """
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')
    # Читаем содержимое JSON
    with open(full_file_path, "r", encoding="utf-8") as userprofile:
        userdata = rapidjson.load(userprofile)

    if len(userdata) > 4:
        return True
    return False


def check_and_create_profile(user_id: str, session_id: str):
    """
    Функция проверяет наличие профайла пользователя в ./userfiles
    и создает словарь с исходными значений.
    """
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')
    profile_exist = os.path.isfile(full_file_path)
    if not profile_exist:
        default_content = {
            "user_id": user_id,
            "user_name": None,
            "allscores": 0,
        }
        default_content_json = rapidjson.dumps(default_content, indent=4)
        # запись данных JSON в файл
        with open(full_file_path, "w", encoding="utf-8") as new_profile:
            new_profile.write(default_content_json)

        new_user_logger = logging.getLogger('new_user_created')
        new_user_logger.setLevel(logging.INFO)
        new_user_handler = logging.FileHandler(filename='logging/new_users.log')
        new_user_formatter = logging.Formatter("%(name)s||%(asctime)s||%(levelname)s||%(message)s")
        new_user_handler.setFormatter(new_user_formatter)
        new_user_logger.addHandler(new_user_handler)
        new_user_logger.info(f'{user_id[-10:]} added')


def check_and_add_new_session(user_id: str, session_id: str):
    """
    Функция открывает профайл пользователя и создает словарь с исходными значений по сессии.
    Должна следовать после выполнения функции check_and_create_profile(),
    но в случая исключения (FileNotFoundError) ссылается на ее повторное выполнение.
    """
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')
    # Читаем содержимое JSON
    try:
        with open(full_file_path, "r", encoding="utf-8") as userprofile:
            userdata = rapidjson.load(userprofile)
    except FileNotFoundError:
        check_and_create_profile(user_id, session_id)

    if not userdata.get(session_id, {}):
        # Добавляем сессию
        time_st = datetime.datetime.utcnow()
        userdata[session_id] = {"time_st": str(time_st),
                                "time_end": None,
                                "time_session": None,
                                "scores": 0
                                }

        # Перезаписываем содержимое
        with open(full_file_path, "w+", encoding="utf-8") as userprofile:
            userprofile.write(rapidjson.dumps(userdata, indent=4))


def get_scores_rating(user_id: str, session_id: str) -> dict:
    """
    Функция просматривает профайл пользователя и возвращает словарь с
    ключ-значениями общего счёта и счёта за сессию.
    """
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')
    with open(full_file_path, "r", encoding="utf-8") as userprofile:
        userdata = rapidjson.load(userprofile)

    allscores = userdata["allscores"]
    sessionscore = userdata[session_id]["scores"]

    return {"allscores": allscores,
            "sessionscore": sessionscore
            }


def update_scores(user_id: str, session_id: str, score: int) -> dict:
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')
    # Читаем содержимое JSON
    with open(full_file_path, "r", encoding="utf-8") as userprofile:
        userdata = rapidjson.load(userprofile)

    # Обрабатываем содержимое
    userdata["allscores"] += score
    userdata[session_id]["scores"] += score

    # Перезаписываем содержимое
    with open(full_file_path, "w+", encoding="utf-8") as userprofile:
        userprofile.write(rapidjson.dumps(userdata, indent=4))

    # print(f'Scores updated {user_id[-10:]}:{session_id[-10:]}')
    return {"allscores": userdata["allscores"],
            "sessionscore": userdata[session_id]["scores"]
            }


def update_time_end(user_id, session_id):
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')
    with open(full_file_path, "r", encoding="utf-8") as userprofile:
        userdata = rapidjson.load(userprofile)

    # Обрабатываем содержимое
    time_end = datetime.datetime.utcnow()
    userdata[session_id]["time_end"] = str(time_end)

    format = '%Y-%m-%d %H:%M:%S.%f'
    time_st = datetime.datetime.strptime(userdata[session_id]["time_st"], format)
    time_end = datetime.datetime.strptime(userdata[session_id]["time_end"], format)
    time_session_t = time_end - time_st
    time_session = time_session_t.total_seconds()

    userdata[session_id]["time_session"] = time_session

    # Перезаписываем содержимое
    with open(full_file_path, "w+", encoding="utf-8") as userprofile:
        userprofile.write(rapidjson.dumps(userdata, indent=4))

    return full_file_path



if __name__ == '__main__':
    user_id = 'D7F19A5927029C89800AC348D6764786EC3F63C084FF7371CB87C3FBDAA37F56'
    session_id = 'a6803c77-9cac-42e5-88ca-108cb1cecc80'
    check_and_create_profile(user_id, session_id)
    check_and_add_new_session(user_id, session_id)
    time.sleep(1.0)
    update_time_end(user_id, session_id)
    session_id = '364c6e58-6578-48a3-847c-e5885d0aa6ec'
    check_and_add_new_session(user_id, session_id)
    update_scores(user_id, session_id, 3)
    update_scores(user_id, session_id, 1)
    update_time_end(user_id, session_id)
    session_id = 'a655311b-1633-4121-bfd7-862a8913e849'
    check_and_add_new_session(user_id, session_id)
    update_scores(user_id, session_id, 2)
    update_time_end(user_id, session_id)
