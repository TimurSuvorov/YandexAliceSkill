import json
import random
import os
from pprint import pprint

from ITsleng.settings import BASE_DIR


def bye_replies():
    # Случайный выбор из файла
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, '../db_sentences.json'), 'r') as fp:
        sentences = json.load(fp)

    bye_text = random.choice(sentences["BYEsentence"])

    response: dict = {
            'text': bye_text,
            'tts': bye_text,
            'end_session': 'True'
    }

    return response