import os
from operator import itemgetter
from time import time
from typing import TypeVar, List, Dict

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
                userfile_data: dict = rapidjson.load(userfile_fp)
                user_id, userscore = itemgetter("user_id", "allscores")(userfile_data)
                common_rating_result[user_id] = userscore
        except (KeyError, FileNotFoundError):
            pass
    with open(COMMON_RATING_FILE, "w", encoding="utf-8") as common_rating_fp:
        common_rating_fp.write(rapidjson.dumps(common_rating_result, indent=4))


if __name__ == '__main__':
    collect_common_rating()
