import json

import rapidjson
import os

cur_dir = os.path.dirname(os.path.abspath(__file__))


def get_db_sentences() -> dict:
    with open(os.path.join(cur_dir, 'db_sentences.json'), 'r', encoding="utf-8") as fp:
        db_sentences = rapidjson.load(fp)
    return db_sentences


def get_db_sounds() -> dict:
    with open(os.path.join(cur_dir, 'db_sounds.json'), 'r', encoding="utf-8") as fp:
        db_sounds = rapidjson.load(fp)
    return db_sounds


if __name__ == '__main__':
    r = get_db_sentences()
    s = get_db_sounds()
    print(r)
    print(s)