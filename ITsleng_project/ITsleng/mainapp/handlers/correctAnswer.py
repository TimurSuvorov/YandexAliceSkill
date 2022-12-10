import random

from .extract_json import get_db_sentences
from .next_question import next_question


def correctanswer(question_attempt):
    sentences = get_db_sentences()
    nicesentence = random.choice(sentences["NICEsentence"])

    response: dict = {
            'text': f'{nicesentence}. Следующий вопрос: {question_attempt[0]["sentence"]}',
            'tts': f'{nicesentence}. Следующий вопрос: {question_attempt[0]["sentence"]}',
            'end_session': 'False'
    }

    return response

