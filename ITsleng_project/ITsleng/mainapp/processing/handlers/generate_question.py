import random
from pprint import pprint

from mainapp.processing.extract_json import get_db_sentences


def generate_question() -> dict:
    sentences = get_db_sentences()
    question_dict = random.choice(sentences["QA"])
    return question_dict


if __name__ == '__main__':
    f = generate_question()
    pprint(f, sort_dicts=False)