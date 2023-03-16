import datetime
import json
import rapidjson
import os
import time
import logging
from pprint import pprint

cur_dir = os.path.dirname(os.path.abspath(__file__))
USERFOLDER = os.path.join(cur_dir, 'userfiles')


# # Logging for new users
# new_user_logger = logging.getLogger('new_user_created')
# new_user_handler = logging.FileHandler(filename='logging/new_users.log')
# new_user_formatter = logging.Formatter("%(name)s||%(asctime)s||%(levelname)s||%(message)s")
# new_user_logger.setLevel(logging.INFO)
# new_user_handler.setFormatter(new_user_formatter)
# new_user_logger.addHandler(new_user_handler)


def check_old_user(user_id: str, session_id: str):
    """
    Функция открывает профайл пользователя и по количеству ключей проверяет новый пользователь или нет.
    Если ключей больше 4 (исходный сет значений[3] + запись текущей сессии[1])
    """
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')
    # Читаем содержимое JSON

    try:
        with open(full_file_path, "r", encoding="utf-8") as userprofile:
            userdata = rapidjson.load(userprofile)
        if len(userdata) > 4:
            return True
        return False
    except FileNotFoundError:
        return False


def check_and_create_profile(user_id: str, session_id: str):
    """
    Функция проверяет наличие профайла пользователя в ./userfiles и создает
    словарь с исходными значений, если пользователь новый.
    """
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')
    profile_exist = os.path.isfile(full_file_path)
    time_st = datetime.datetime.utcnow()
    if not profile_exist:
        userprofile_content = {
            "user_id": user_id,
            "user_name": None,
            "allscores": 0,
            session_id: {
                "time_st": str(time_st),
                "time_end": None,
                "time_session": None,
                "scores": 0
            }
        }
        # запись данных JSON в файл
        with open(full_file_path, "w", encoding="utf-8") as new_profile:
            new_profile.write(rapidjson.dumps(userprofile_content, indent=4))

        # new_user_logger.info(f'{user_id[-10:]} added')


def check_and_add_new_session(user_id: str, session_id: str):
    """
    Функция открывает профайл пользователя и создает словарь с исходными значениями по сессии.
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
    ключ-значениями общего счёта и счёта за сессию. В случая исключения (FileNotFoundError) файл пользователя
    пересоздается, а баллы отдаются нулевые.
    """
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')
    try:
        with open(full_file_path, "r", encoding="utf-8") as userprofile:
            userdata = rapidjson.load(userprofile)
            allscores = userdata["allscores"]
            sessionscore = userdata[session_id]["scores"]
    except FileNotFoundError:
        check_and_create_profile(user_id, session_id)
        allscores = 0
        sessionscore = 0

    return {"allscores": allscores,
            "sessionscore": sessionscore
            }


def update_scores(user_id: str, session_id: str, score: int) -> dict:
    """
    Функция открывает файл пользователя и обновляет балы общие и за сессию.
    В случая исключения (FileNotFoundError) файл пользователя пересоздается, а баллы отдаются нулевые.
    """
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')

    try:
        with open(full_file_path, "r", encoding="utf-8") as userprofile:
            userdata = rapidjson.load(userprofile)

        userdata["allscores"] += score
        userdata[session_id]["scores"] += score
        allscores = userdata["allscores"]
        sessionscore = userdata[session_id]["scores"]

        with open(full_file_path, "w+", encoding="utf-8") as userprofile:
            userprofile.write(rapidjson.dumps(userdata, indent=4))

    except FileNotFoundError:
        check_and_create_profile(user_id, session_id)
        allscores = 0
        sessionscore = 0

    return {"allscores": allscores,
            "sessionscore": sessionscore
            }


def update_time_end(user_id: str, session_id: str) -> None:
    """
    Функция открывает файл пользователя и обновляет время за сессию на основе время старта сессии.
    В случая исключения (FileNotFoundError) файл пользователя пересоздается
    """
    full_file_path = os.path.join(USERFOLDER, f'{user_id}.json')
    try:
        with open(full_file_path, "r", encoding="utf-8") as userprofile:
            userdata = rapidjson.load(userprofile)

        # Обрабатываем содержимое
        time_end = datetime.datetime.utcnow()
        userdata[session_id]["time_end"] = str(time_end)

        FORMAT = '%Y-%m-%d %H:%M:%S.%f'
        time_st = datetime.datetime.strptime(userdata[session_id]["time_st"], FORMAT)
        time_end = datetime.datetime.strptime(userdata[session_id]["time_end"], FORMAT)
        time_session = (time_end - time_st).total_seconds()

        userdata[session_id]["time_session"] = time_session

        # Перезаписываем содержимое
        with open(full_file_path, "w+", encoding="utf-8") as userprofile:
            userprofile.write(rapidjson.dumps(userdata, indent=4))

    except FileNotFoundError:
        check_and_create_profile(user_id, session_id)


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