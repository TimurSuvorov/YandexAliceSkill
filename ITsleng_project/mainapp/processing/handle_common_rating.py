import os
from operator import itemgetter
from time import time
from typing import TypeVar, List, Dict, Tuple

import rapidjson

PathLike = TypeVar("PathLike", str, os.PathLike)

cur_dir: PathLike = os.path.dirname(__file__)
USERFOLDER: PathLike = os.path.join(cur_dir, 'userfiles')
COMMON_RATING_FILE: PathLike = os.path.join(cur_dir, 'ratingfiles', 'common_rating.json')

TIME_REFRESH_AGO = 60  # Срок обновления userprofile-ов (должен быть больше, чем период сбора) [сек]
TIME_CHECK_AGO = TIME_REFRESH_AGO + 60  # Срок обновления общего файла рейтинга [сек]


def collect_common_rating() -> None:
    """
    Функция предназначена для сбора информации о балах из каждого профайла.

    Периодичность запуска функции должна быть не меньше таймера TIME_REFRESH_AGO, который означает отрезок
    времени изменения просматриваемых профайлов пользователя относительно текущего времени.
    Сбор баллов осуществляется в файл ./ratingfiles/common_rating.json в виде словаря c "user_id": "scores".
    В случае, если `common_rating.json` обновлялся отн-но давно (например, из-за сбоя планировщика) -
    больше, чем таймер TIME_CHECK_AGO - просматриваются все имеющиеся профайлы.
    """

    try:
        with open(COMMON_RATING_FILE, "r", encoding="utf-8") as common_rating_fp:
            common_rating_result: Dict = rapidjson.load(common_rating_fp)
    except FileNotFoundError:
        with open(COMMON_RATING_FILE, "w", encoding="utf-8") as fp:
            pass
        common_rating_result = {}

    userfiles: List[str] = os.listdir(USERFOLDER)
    # По умолчанию обходим все userprofile-ы
    userfiles_for_collect: List[str] = [os.path.join(USERFOLDER, file) for file in userfiles]
    # Если файл общего рейтинга обновлялся недавно относительно обновления профайлов и общий файл рейтинга непустой
    if time() - os.path.getmtime(COMMON_RATING_FILE) < TIME_CHECK_AGO and common_rating_result:
        # Обходим только userprofile-ы со свежими изменениями
        userfiles_for_collect: List = \
            list(filter(lambda file: time() - os.path.getmtime(file) < TIME_REFRESH_AGO, userfiles_for_collect))
    for file in userfiles_for_collect:
        try:
            with open(file, "r", encoding="utf-8") as userfile_fp:
                userfile_data: Dict = rapidjson.load(userfile_fp)
                user_id, userscore = itemgetter("user_id", "allscores")(userfile_data)
                common_rating_result[user_id] = userscore
        except (KeyError, FileNotFoundError):
            pass
    common_rating_result_sorted: Dict[str, int] = dict(sorted(common_rating_result.items(),
                                                              key=lambda item: item[1],
                                                              reverse=True)
                                                       )
    with open(COMMON_RATING_FILE, "w", encoding="utf-8") as common_rating_fp:
        common_rating_fp.write(rapidjson.dumps(common_rating_result_sorted, indent=4))


def get_user_common_rating_info(user_id: str) -> Tuple[List[int], str]:
    """
    Функция получает информацию о месте в общем рейтинге и количество балов для пользователя.
    Также формирует таблицу рейтинга.
    """
    with open(COMMON_RATING_FILE, "r", encoding="utf-8") as com_rat_fp:
        com_rat_data: dict = rapidjson.load(com_rat_fp)
    # Находим место в общем рейтинге из упорядоченного словаря по позиции
    usersid_list: List[str] = list(com_rat_data.keys())
    usersid_scores_list: List[Tuple[str, int]] = list(com_rat_data.items())
    user_place_score: List[int] = [usersid_list.index(user_id) + 1, com_rat_data.get(user_id)]

    # Формирование таблицы рейтинга
    rating_table_print: str = "Таблица рейтинга:"
    for index, userid_scores in enumerate(usersid_scores_list[:3]):
        rating_table_print += f'\n{index + 1}-е место: {userid_scores[1]}'
        if userid_scores[0] == user_id:
            rating_table_print += " 👈👈"

    if user_place_score[0] == 4:
        rating_table_print += f'\n{user_place_score[0]}-е место: {user_place_score[1]} 👈👈'
    if user_place_score[0] == 5:
        rating_table_print += f'\n4-е место: {usersid_scores_list[3][1]}'
        rating_table_print += f'\n{user_place_score[0]}-е место: {user_place_score[1]} 👈👈'
    if user_place_score[0] > 5:
        rating_table_print += f'\n...\n{user_place_score[0]}-е место: {user_place_score[1]} 👈👈'
    rating_table_print += "\n...\n"
    return user_place_score, rating_table_print


