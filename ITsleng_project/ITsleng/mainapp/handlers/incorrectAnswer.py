import random

from .extract_json import get_db_sentences
from .generate_question import generate_question


def incorrectanswer(question_attempt):

    sentences = get_db_sentences()

    if question_attempt[1] > 0:
        mistakesentence = random.choice(sentences["MISTAKEsentence"])
        response: dict = {
                'text': f'{mistakesentence}',
                'tts': f'{mistakesentence}',
                'end_session': 'False'
        }
        question_attempt = (question_attempt[0], question_attempt[1] - 1)
    else:
        badsentence = random.choice(sentences["BADsentence"])
        question_answers = question_attempt[0]["answers"]
        question_attempt = generate_question()
        response: dict = {
                'text': f'{badsentence}: {question_answers[0]}. Следующий вопрос: {question_attempt[0]["sentence"]}',
                'tts': f'{badsentence}: {question_answers[0]}. Следующий вопрос: {question_attempt[0]["sentence"]}',
                'end_session': 'False'
        }

    return response, question_attempt
