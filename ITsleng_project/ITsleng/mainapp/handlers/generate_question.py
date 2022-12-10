import random
from .extract_json import get_db_sentences

def generate_question():
    sentences = get_db_sentences()
    question = random.choice(sentences["QA"])
    attempt = 1

    return question, attempt
