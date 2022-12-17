import datetime
import json
import os
import time
from pprint import pprint


def check_exist_profile(user_id: str) -> bool:
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    full_file_path = os.path.join(cur_dir, f'{user_id}.json')
    exist = os.path.isfile(full_file_path)
    return exist


def create_default_profile(user_id, session_id, time_st=datetime.datetime.utcnow()):
    default_content = {
        "user_id": user_id,
        "user_name": None,
        "allscores": 0,
         session_id: {}
    }
    default_content_json = json.dumps(default_content)
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    full_file_path = os.path.join(cur_dir, f'{user_id}.json')
    # запись данных JSON в файл
    with open(full_file_path, "w", encoding="utf-8") as new_profile:
        new_profile.write(default_content_json)
        print(f'Created new profile {user_id[-10:]}')
    return full_file_path


def add_new_session(user_id, session_id):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    full_file_path = os.path.join(cur_dir, f'{user_id}.json')
    # Читаем содержимое JSON
    with open(full_file_path, "r", encoding="utf-8") as userprofile:
        userdata = json.load(userprofile)

    # Обрабатываем содержимое
    time_st = datetime.datetime.utcnow()
    userdata[session_id] = {"time_st": str(time_st),
                            "time_end": None,
                            "time_session": None,
                            "scores": 0
                            }

    # Перезаписываем содержимое
    with open(full_file_path, "w+", encoding="utf-8") as userprofile:
        userprofile.write(json.dumps(userdata))

    print(f'Add new session {user_id[-10:]}:{session_id[-10:]}')
    return full_file_path


def update_scores(user_id, session_id, score):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    full_file_path = os.path.join(cur_dir, f'{user_id}.json')
    # Читаем содержимое JSON
    with open(full_file_path, "r", encoding="utf-8") as userprofile:
        userdata = json.load(userprofile)

    # Обрабатываем содержимое
    userdata["allscores"] += score
    userdata[session_id]["scores"] += score

    # Перезаписываем содержимое
    with open(full_file_path, "w+", encoding="utf-8") as userprofile:
        userprofile.write(json.dumps(userdata))

    print(f'Scores updated {user_id[-10:]}:{session_id[-10:]}')
    return full_file_path

def update_time_end(user_id, session_id):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    full_file_path = os.path.join(cur_dir, f'{user_id}.json')
    # Читаем содержимое JSON
    with open(full_file_path, "r", encoding="utf-8") as userprofile:
        userdata = json.load(userprofile)

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
        userprofile.write(json.dumps(userdata))

    print(f'Last_time updated {user_id[-10:]}:{session_id[-10:]}')
    return full_file_path

if __name__ == '__main__':
    user_id = 'D7F19A5927029C89800AC348D6764786EC3F63C084FF7371CB87C3FBDAA37F56'
    session_id = 'a6803c77-9cac-42e5-88ca-108cb1cecc80'
    create_default_profile(user_id, session_id)
    add_new_session(user_id, session_id)
    session_id = '364c6e58-6578-48a3-847c-e5885d0aa6ec'
    add_new_session(user_id, session_id)
    update_scores(user_id, session_id, 3)
    update_scores(user_id, session_id, 1)
    session_id = 'a655311b-1633-4121-bfd7-862a8913e849'
    add_new_session(user_id, session_id)
    update_scores(user_id, session_id, 2)
    time.sleep(10)
    update_time_end(user_id, session_id)