from functools import lru_cache

import rapidjson
import os

cur_dir = os.path.dirname(os.path.abspath(__file__))


@lru_cache()
def get_db_sentences() -> dict:
    with open(os.path.join(cur_dir, 'db_sentences.json'), 'r', encoding="utf-8") as fp:
        db_sentences = rapidjson.load(fp)
    return db_sentences


@lru_cache
def get_db_sounds() -> dict:
    with open(os.path.join(cur_dir, 'db_sounds.json'), 'r', encoding="utf-8") as fp:
        db_sounds = rapidjson.load(fp)
    return db_sounds