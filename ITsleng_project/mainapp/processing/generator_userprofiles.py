import os
import string

import rapidjson
import random
from typing import TypeVar

PathLike = TypeVar("PathLike", str, os.PathLike)

cur_dir: PathLike = os.path.dirname(__file__)
USERFOLDER: PathLike = os.path.join(cur_dir, 'userfiles')


def user_id_generator():
    numbers = string.digits
    capital_words = string.ascii_uppercase
    s = numbers + capital_words
    user_id = ''.join([random.choice(s) for _ in range(64)])
    return user_id


def generator_userprofiles(user_id: str) -> None:
    full_file_path: PathLike = os.path.join(USERFOLDER, f'{user_id}.json')
    userprofile_content = {
        "user_id": user_id,
        "user_name": None,
        "allscores": random.randint(3, 250),
    }
    with open(full_file_path, "w", encoding="utf-8") as new_profile:
        new_profile.write(rapidjson.dumps(userprofile_content, indent=4))


if __name__ == '__main__':
    for _ in range(100):
        generator_userprofiles(user_id=user_id_generator())
