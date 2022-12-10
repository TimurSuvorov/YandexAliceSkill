import random
from pprint import pprint

from .extract_json import get_db_sentences


def next_question(question_tuple):

    question_body = question_tuple[0]["sentence"]

    response: dict = {
            'text': question_body,
            'tts': question_body,
            'end_session': 'False'
    }

    return response

if __name__ == '__main__':
    s = ["нет, не"]

    i = "неа"
    print(i in s)
