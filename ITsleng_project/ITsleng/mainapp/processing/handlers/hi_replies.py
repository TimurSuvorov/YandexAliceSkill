import random
from pprint import pprint
from mainapp.processing.extract_json import get_db_sentences

def hi_replies():
    sentences = get_db_sentences()

    # Случайный выбор фразы
    hi_text = random.choice(sentences["HIsentence"])

    response: dict = {
            'text': hi_text,
            'buttons': [
                {'title': 'Помощь', 'hide': 'true'},
                {'title': 'Что ты умеешь?', 'hide': 'true'}
            ],
            'tts': hi_text,
            'end_session': 'false'
    }

    return response