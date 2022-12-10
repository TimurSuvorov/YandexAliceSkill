import json
import os


def get_db_sentences() -> dict:
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, 'db_sentences.json'), 'r') as fp:
        db_sentences = json.load(fp)
    return db_sentences
